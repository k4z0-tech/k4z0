"""
Order Analysis Agent
Analyzes delivery delays, gathers feedback, and learns from past actions.
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json
import os


class OrderAgent:
    """
    Intelligent agent for analyzing order delivery delays and learning from feedback.
    """

    def __init__(self, data_file: str = "order_train_data.xlsx"):
        """
        Initialize the OrderAgent.

        Args:
            data_file: Path to the Excel file containing order data
        """
        self.data_file = data_file
        self.orders_df = None
        self.delayed_orders = []
        self.feedback_history = []
        self.learned_actions = {}
        self.feedback_file = "feedback_history.json"
        self.load_data()
        self.load_feedback_history()

    def load_data(self):
        """Load order data from Excel file."""
        try:
            self.orders_df = pd.read_excel(self.data_file)
            print(f"✅ Loaded {len(self.orders_df)} orders from {self.data_file}")
            print(f"📊 Columns: {list(self.orders_df.columns)}")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.orders_df = pd.DataFrame()

    def load_feedback_history(self):
        """Load previous feedback and learned actions."""
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r') as f:
                    data = json.load(f)
                    self.feedback_history = data.get('feedback_history', [])
                    self.learned_actions = data.get('learned_actions', {})
                print(f"📚 Loaded {len(self.feedback_history)} previous feedback entries")
            except Exception as e:
                print(f"⚠️  Error loading feedback history: {e}")

    def save_feedback_history(self):
        """Save feedback and learned actions to file."""
        data = {
            'feedback_history': self.feedback_history,
            'learned_actions': self.learned_actions,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.feedback_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"💾 Saved feedback history to {self.feedback_file}")

    def analyze_delivery_tat(self, tat_threshold_days: int = 3) -> List[Dict[str, Any]]:
        """
        Analyze Delivery TAT and identify delayed orders.

        Args:
            tat_threshold_days: Threshold in days for considering an order delayed

        Returns:
            List of delayed orders with details
        """
        if self.orders_df.empty:
            print("❌ No data available for analysis")
            return []

        # Find the Delivery TAT column (case-insensitive search)
        tat_column = None
        for col in self.orders_df.columns:
            if 'delivery' in col.lower() and 'tat' in col.lower():
                tat_column = col
                break

        if tat_column is None:
            print("❌ Could not find 'Delivery TAT' column in the data")
            print(f"Available columns: {list(self.orders_df.columns)}")
            return []

        print(f"📈 Analyzing column: {tat_column}")

        # Convert TAT to numeric, handling various formats
        self.orders_df['TAT_numeric'] = pd.to_numeric(
            self.orders_df[tat_column], errors='coerce'
        )

        # Filter delayed orders (TAT > threshold days)
        delayed_mask = self.orders_df['TAT_numeric'] > tat_threshold_days
        delayed_df = self.orders_df[delayed_mask].copy()

        if delayed_df.empty:
            print(f"✅ No orders with Delivery TAT > {tat_threshold_days} days found")
            return []

        print(f"⚠️  Found {len(delayed_df)} delayed orders (TAT > {tat_threshold_days} days)")

        # Convert to list of dictionaries
        self.delayed_orders = []
        for idx, row in delayed_df.iterrows():
            order = {
                'order_id': row.get('Order ID', row.get('order_id', f'Order_{idx}')),
                'delivery_tat': row['TAT_numeric'],
                'tat_column': tat_column,
                'original_data': row.to_dict()
            }
            self.delayed_orders.append(order)

        return self.delayed_orders

    def display_delayed_orders(self):
        """Display delayed orders to the user."""
        if not self.delayed_orders:
            print("📭 No delayed orders to display")
            return

        print("\n" + "="*80)
        print("🚨 DELAYED ORDERS ALERT")
        print("="*80)
        print(f"Total delayed orders: {len(self.delayed_orders)}")
        print(f"Threshold: > 3 days Delivery TAT")
        print("="*80 + "\n")

        for i, order in enumerate(self.delayed_orders, 1):
            print(f"📦 Order {i}:")
            print(f"   Order ID: {order['order_id']}")
            print(f"   Delivery TAT: {order['delivery_tat']} days")
            print(f"   Status: DELAYED")
            print()

    def gather_feedback(self, order_id: str) -> Dict[str, Any]:
        """
        Gather feedback from user about a delayed order.

        Args:
            order_id: The order ID to gather feedback for

        Returns:
            Dictionary containing user feedback
        """
        print(f"\n{'='*60}")
        print(f"📝 FEEDBACK FOR ORDER: {order_id}")
        print(f"{'='*60}")

        # Check if we have previous feedback for similar orders
        similar_actions = self.get_similar_actions(order_id)
        if similar_actions:
            print(f"\n💡 Based on previous experience, here are some suggestions:")
            for i, action in enumerate(similar_actions[:3], 1):
                print(f"   {i}. {action['action']} (worked {action['success_rate']}% of the time)")

        print("\nPlease answer the following questions:")
        print("-"*60)

        # Question 1: Why was the order delayed?
        delay_reason = input("\n1. Why was this order delayed?\n   Your answer: ").strip()

        # Question 2: What actions did you take?
        print("\n2. What actions did you take to speed up/complete the delivery?")
        print("   (You can list multiple actions, separated by commas)")
        actions_taken = input("   Your answer: ").strip()

        # Question 3: Were the actions successful?
        success = input("\n3. Were your actions successful? (yes/no/partially): ").strip().lower()

        # Question 4: Additional notes
        additional_notes = input("\n4. Any additional notes or lessons learned?\n   Your answer: ").strip()

        feedback = {
            'order_id': order_id,
            'timestamp': datetime.now().isoformat(),
            'delay_reason': delay_reason,
            'actions_taken': [a.strip() for a in actions_taken.split(',')],
            'success': success,
            'additional_notes': additional_notes
        }

        return feedback

    def process_feedback(self, feedback: Dict[str, Any]):
        """
        Process and store feedback, update learned actions.

        Args:
            feedback: Feedback dictionary from user
        """
        # Store feedback
        self.feedback_history.append(feedback)

        # Update learned actions
        for action in feedback['actions_taken']:
            if action not in self.learned_actions:
                self.learned_actions[action] = {
                    'success_count': 0,
                    'total_count': 0,
                    'success_rate': 0,
                    'related_reasons': []
                }

            self.learned_actions[action]['total_count'] += 1
            if feedback['success'] in ['yes', 'partially']:
                self.learned_actions[action]['success_count'] += 1

            # Update success rate
            total = self.learned_actions[action]['total_count']
            successes = self.learned_actions[action]['success_count']
            self.learned_actions[action]['success_rate'] = round((successes / total) * 100, 1)

            # Track related delay reasons
            if feedback['delay_reason'] not in self.learned_actions[action]['related_reasons']:
                self.learned_actions[action]['related_reasons'].append(feedback['delay_reason'])

        # Save to file
        self.save_feedback_history()

        print(f"\n✅ Feedback recorded successfully!")
        print(f"📊 Total feedback entries: {len(self.feedback_history)}")
        print(f"🎯 Learned actions: {len(self.learned_actions)}")

    def get_similar_actions(self, order_id: str) -> List[Dict[str, Any]]:
        """
        Get similar actions based on order characteristics.

        Args:
            order_id: Order ID to find similar actions for

        Returns:
            List of recommended actions with success rates
        """
        if not self.learned_actions:
            return []

        # Find the order in our data
        order_data = None
        for order in self.delayed_orders:
            if order['order_id'] == order_id:
                order_data = order
                break

        if not order_data:
            return []

        # Get all actions sorted by success rate
        sorted_actions = sorted(
            self.learned_actions.items(),
            key=lambda x: x[1]['success_rate'],
            reverse=True
        )

        return [
            {
                'action': action,
                'success_rate': data['success_rate'],
                'total_uses': data['total_count']
            }
            for action, data in sorted_actions[:5]  # Top 5 actions
        ]

    def generate_report(self) -> str:
        """
        Generate a comprehensive analysis report.

        Returns:
            Report string
        """
        report = []
        report.append("="*80)
        report.append("📊 ORDER ANALYSIS REPORT")
        report.append("="*80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # Summary
        report.append("📈 SUMMARY:")
        report.append(f"   Total orders analyzed: {len(self.orders_df)}")
        report.append(f"   Delayed orders (>3 days TAT): {len(self.delayed_orders)}")
        report.append(f"   Delay rate: {len(self.delayed_orders)/len(self.orders_df)*100:.1f}%")
        report.append("")

        # Delayed orders details
        if self.delayed_orders:
            report.append("🚨 DELAYED ORDERS:")
            for i, order in enumerate(self.delayed_orders, 1):
                report.append(f"   {i}. Order ID: {order['order_id']}")
                report.append(f"      Delivery TAT: {order['delivery_tat']} days")
            report.append("")

        # Learned actions
        if self.learned_actions:
            report.append("📚 LEARNED ACTIONS (from previous feedback):")
            sorted_actions = sorted(
                self.learned_actions.items(),
                key=lambda x: x[1]['success_rate'],
                reverse=True
            )
            for i, (action, data) in enumerate(sorted_actions[:10], 1):
                report.append(f"   {i}. {action}")
                report.append(f"      Success rate: {data['success_rate']}%")
                report.append(f"      Used {data['total_count']} times")
            report.append("")

        # Feedback history
        if self.feedback_history:
            report.append(f"📝 FEEDBACK HISTORY: {len(self.feedback_history)} entries")
            report.append("")

        report.append("="*80)
        return "\n".join(report)

    def provide_guidance(self, order_id: str) -> str:
        """
        Provide guidance based on learned actions for a specific order.

        Args:
            order_id: Order ID to provide guidance for

        Returns:
            Guidance string
        """
        if not self.learned_actions:
            return "📚 No previous feedback available yet. Please provide feedback to help me learn."

        similar_actions = self.get_similar_actions(order_id)
        if not similar_actions:
            return "📚 No similar actions found for this order type."

        guidance = []
        guidance.append(f"\n💡 GUIDANCE FOR ORDER {order_id}:")
        guidance.append("="*60)
        guidance.append("Based on previous feedback, here are recommended actions:")
        guidance.append("")

        for i, action in enumerate(similar_actions, 1):
            guidance.append(f"{i}. {action['action']}")
            guidance.append(f"   Success rate: {action['success_rate']}%")
            guidance.append(f"   Used {action['total_uses']} times")
            guidance.append("")

        guidance.append("="*60)
        return "\n".join(guidance)

    def run_analysis(self):
        """Main method to run the complete analysis workflow."""
        print("\n" + "="*80)
        print("🤖 ORDER ANALYSIS AGENT")
        print("="*80)
        print("Starting comprehensive order analysis...")
        print("="*80 + "\n")

        # Step 1: Analyze delivery TAT
        print("📊 Step 1: Analyzing Delivery TAT...")
        delayed_orders = self.analyze_delivery_tat()

        if not delayed_orders:
            print("\n✅ All orders are within acceptable delivery times!")
            print("   No further action needed.")
            return

        # Step 2: Display delayed orders
        print("\n📋 Step 2: Displaying delayed orders...")
        self.display_delayed_orders()

        # Step 3: Gather feedback for each delayed order
        print("\n📝 Step 3: Gathering feedback for delayed orders...")
        for order in self.delayed_orders:
            order_id = order['order_id']

            # Provide guidance based on learned actions
            guidance = self.provide_guidance(order_id)
            print(guidance)

            # Gather feedback
            feedback = self.gather_feedback(order_id)

            # Process and store feedback
            self.process_feedback(feedback)

            print(f"\n✅ Feedback recorded for order {order_id}")

        # Step 4: Generate report
        print("\n📊 Step 4: Generating analysis report...")
        report = self.generate_report()
        print(report)

        # Step 5: Save report to file
        report_file = f"order_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"\n💾 Report saved to: {report_file}")

        print("\n" + "="*80)
        print("✅ ANALYSIS COMPLETE")
        print("="*80)
        print(f"📊 Analyzed {len(self.orders_df)} orders")
        print(f"⚠️  Found {len(self.delayed_orders)} delayed orders")
        print(f"📝 Collected feedback for all delayed orders")
        print(f"📚 Learned {len(self.learned_actions)} actionable strategies")
        print("="*80 + "\n")


def main():
    """Main entry point for the order analysis agent."""
    agent = OrderAgent("order_train_data.xlsx")
    agent.run_analysis()


if __name__ == "__main__":
    main()
