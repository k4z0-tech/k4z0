"""
Order Analysis Agent - Interactive Version
Handles large numbers of delayed orders by processing in batches
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json
import os
import sys


class OrderAgentInteractive:
    """
    Interactive agent that processes delayed orders in manageable batches.
    """

    def __init__(self, data_file: str = "order_train_data.xlsx"):
        self.data_file = data_file
        self.orders_df = None
        self.delayed_orders = []
        self.feedback_history = []
        self.learned_actions = {}
        self.feedback_file = "feedback_history.json"
        self.batch_size = 10  # Process orders in batches of 10
        self.load_data()
        self.load_feedback_history()

    def load_data(self):
        """Load order data from Excel file."""
        try:
            self.orders_df = pd.read_excel(self.data_file)
            print(f"[OK] Loaded {len(self.orders_df)} orders from {self.data_file}")
        except Exception as e:
            print(f"[ERROR] Error loading data: {e}")
            self.orders_df = pd.DataFrame()

    def load_feedback_history(self):
        """Load previous feedback and learned actions."""
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r') as f:
                    data = json.load(f)
                    self.feedback_history = data.get('feedback_history', [])
                    self.learned_actions = data.get('learned_actions', {})
                print(f"[INFO] Loaded {len(self.feedback_history)} previous feedback entries")
            except Exception as e:
                print(f"[WARNING] Error loading feedback history: {e}")

    def save_feedback_history(self):
        """Save feedback and learned actions to file."""
        data = {
            'feedback_history': self.feedback_history,
            'learned_actions': self.learned_actions,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.feedback_file, 'w') as f:
            json.dump(data, f, indent=2)

    def analyze_delivery_tat(self, tat_threshold_days: int = 3) -> List[Dict[str, Any]]:
        """Analyze Delivery TAT and identify delayed orders."""
        if self.orders_df.empty:
            print("[ERROR] No data available for analysis")
            return []

        # Find the Delivery TAT column
        tat_column = None
        for col in self.orders_df.columns:
            if 'delivery' in col.lower() and 'tat' in col.lower():
                tat_column = col
                break

        if tat_column is None:
            print("[ERROR] Could not find 'Delivery TAT' column")
            return []

        print(f"[INFO] Analyzing column: {tat_column}")

        # Convert TAT to numeric
        self.orders_df['TAT_numeric'] = pd.to_numeric(
            self.orders_df[tat_column], errors='coerce'
        )

        # Filter delayed orders
        delayed_mask = self.orders_df['TAT_numeric'] > tat_threshold_days
        delayed_df = self.orders_df[delayed_mask].copy()

        if delayed_df.empty:
            print(f"[OK] No orders with Delivery TAT > {tat_threshold_days} days found")
            return []

        print(f"[WARNING] Found {len(delayed_df)} delayed orders (TAT > {tat_threshold_days} days)")

        # Convert to list of dictionaries
        self.delayed_orders = []
        for idx, row in delayed_df.iterrows():
            order_id = row.get('Source Document Number', row.get('Order ID', f'Order_{idx}'))
            order = {
                'order_id': order_id,
                'delivery_tat': row['TAT_numeric'],
                'tat_column': tat_column,
                'original_data': row.to_dict()
            }
            self.delayed_orders.append(order)

        return self.delayed_orders

    def display_summary(self):
        """Display summary of delayed orders."""
        if not self.delayed_orders:
            print("[INFO] No delayed orders to display")
            return

        print("\n" + "="*70)
        print("DELAYED ORDERS SUMMARY")
        print("="*70)
        print(f"Total delayed orders: {len(self.delayed_orders)}")
        print(f"Threshold: > 3 days Delivery TAT")
        print(f"Batch size: {self.batch_size} orders per batch")
        print("="*70)

        # Show statistics
        tat_values = [o['delivery_tat'] for o in self.delayed_orders]
        print(f"\nStatistics:")
        print(f"  Average TAT: {sum(tat_values)/len(tat_values):.1f} days")
        print(f"  Min TAT: {min(tat_values)} days")
        print(f"  Max TAT: {max(tat_values)} days")
        print(f"  Orders > 30 days: {sum(1 for t in tat_values if t > 30)}")
        print(f"  Orders > 60 days: {sum(1 for t in tat_values if t > 60)}")
        print()

    def get_similar_actions(self, order_id: str) -> List[Dict[str, Any]]:
        """Get similar actions based on past feedback."""
        if not self.learned_actions:
            return []

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
            for action, data in sorted_actions[:5]
        ]

    def gather_feedback(self, order_id: str, batch_num: int, total_batches: int) -> Dict[str, Any]:
        """Gather feedback from user about a delayed order."""
        print(f"\n{'='*70}")
        print(f"FEEDBACK FOR ORDER: {order_id}")
        print(f"Batch {batch_num}/{total_batches}")
        print(f"{'='*70}")

        # Show learned actions if available
        similar_actions = self.get_similar_actions(order_id)
        if similar_actions:
            print(f"\n[TIP] Based on previous experience:")
            for i, action in enumerate(similar_actions[:3], 1):
                print(f"   {i}. {action['action']} (worked {action['success_rate']}% of the time)")

        print("\nPlease answer the following questions:")
        print("-"*70)

        # Question 1
        delay_reason = input("\n1. Why was this order delayed?\n   Your answer: ").strip()

        # Question 2
        print("\n2. What actions did you take to speed up/complete the delivery?")
        print("   (You can list multiple actions, separated by commas)")
        actions_taken = input("   Your answer: ").strip()

        # Question 3
        success = input("\n3. Were your actions successful? (yes/no/partially): ").strip().lower()

        # Question 4
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
        """Process and store feedback, update learned actions."""
        self.feedback_history.append(feedback)

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

            total = self.learned_actions[action]['total_count']
            successes = self.learned_actions[action]['success_count']
            self.learned_actions[action]['success_rate'] = round((successes / total) * 100, 1)

            if feedback['delay_reason'] not in self.learned_actions[action]['related_reasons']:
                self.learned_actions[action]['related_reasons'].append(feedback['delay_reason'])

        self.save_feedback_history()

    def run_analysis(self):
        """Main method to run the complete analysis workflow."""
        print("\n" + "="*70)
        print("ORDER ANALYSIS AGENT - INTERACTIVE MODE")
        print("="*70)
        print("Starting comprehensive order analysis...")
        print("="*70 + "\n")

        # Step 1: Analyze delivery TAT
        print("[STEP 1] Analyzing Delivery TAT...")
        delayed_orders = self.analyze_delivery_tat()

        if not delayed_orders:
            print("\n[OK] All orders are within acceptable delivery times!")
            return

        # Step 2: Display summary
        print("\n[STEP 2] Displaying summary...")
        self.display_summary()

        # Step 3: Ask user how many orders to process
        print("\n[STEP 3] Processing delayed orders...")
        total_orders = len(self.delayed_orders)
        total_batches = (total_orders + self.batch_size - 1) // self.batch_size

        print(f"\nYou have {total_orders} delayed orders.")
        print(f"They will be processed in batches of {self.batch_size}.")
        print(f"Total batches: {total_batches}")

        # Ask user which batch to start with
        print("\nOptions:")
        print("  1. Process all orders (may take a while)")
        print("  2. Process first batch only")
        print("  3. Skip feedback collection")
        print("  4. Exit")

        choice = input("\nYour choice (1-4): ").strip()

        if choice == '4':
            print("\nExiting...")
            return

        if choice == '3':
            print("\nSkipping feedback collection...")
            report = self.generate_report()
            print(report)
            return

        # Process orders
        if choice == '2':
            # Process first batch only
            batch_orders = self.delayed_orders[:self.batch_size]
            print(f"\nProcessing first batch ({len(batch_orders)} orders)...")
            self.process_batch(batch_orders, 1, 1)
        else:
            # Process all orders in batches
            for batch_num in range(1, total_batches + 1):
                start_idx = (batch_num - 1) * self.batch_size
                end_idx = min(start_idx + self.batch_size, total_orders)
                batch_orders = self.delayed_orders[start_idx:end_idx]

                print(f"\n{'='*70}")
                print(f"BATCH {batch_num}/{total_batches}")
                print(f"Processing orders {start_idx + 1} to {end_idx}")
                print(f"{'='*70}")

                self.process_batch(batch_orders, batch_num, total_batches)

                # Ask if user wants to continue
                if batch_num < total_batches:
                    continue_choice = input(f"\nContinue to next batch? (yes/no): ").strip().lower()
                    if continue_choice != 'yes':
                        print("\nStopping batch processing...")
                        break

        # Generate report
        print("\n[STEP 4] Generating analysis report...")
        report = self.generate_report()
        print(report)

        # Save report
        report_file = f"order_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"\n[SAVED] Report saved to: {report_file}")

        print("\n" + "="*70)
        print("ANALYSIS COMPLETE")
        print("="*70)
        print(f"[STATS] Analyzed {len(self.orders_df)} orders")
        print(f"[STATS] Found {len(self.delayed_orders)} delayed orders")
        print(f"[STATS] Collected feedback for processed orders")
        print(f"[STATS] Learned {len(self.learned_actions)} actionable strategies")
        print("="*70 + "\n")

    def process_batch(self, batch_orders: List[Dict], batch_num: int, total_batches: int):
        """Process a batch of orders."""
        for i, order in enumerate(batch_orders, 1):
            order_id = order['order_id']
            print(f"\nProcessing order {i}/{len(batch_orders)} in batch {batch_num}")

            # Gather feedback
            feedback = self.gather_feedback(order_id, batch_num, total_batches)

            # Process feedback
            self.process_feedback(feedback)

            print(f"[OK] Feedback recorded for order {order_id}")

    def generate_report(self) -> str:
        """Generate a comprehensive analysis report."""
        report = []
        report.append("="*70)
        report.append("ORDER ANALYSIS REPORT")
        report.append("="*70)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # Summary
        report.append("SUMMARY:")
        report.append(f"   Total orders analyzed: {len(self.orders_df)}")
        report.append(f"   Delayed orders (>3 days TAT): {len(self.delayed_orders)}")
        if len(self.orders_df) > 0:
            report.append(f"   Delay rate: {len(self.delayed_orders)/len(self.orders_df)*100:.1f}%")
        report.append("")

        # Statistics
        if self.delayed_orders:
            tat_values = [o['delivery_tat'] for o in self.delayed_orders]
            report.append("STATISTICS:")
            report.append(f"   Average TAT: {sum(tat_values)/len(tat_values):.1f} days")
            report.append(f"   Min TAT: {min(tat_values)} days")
            report.append(f"   Max TAT: {max(tat_values)} days")
            report.append("")

        # Learned actions
        if self.learned_actions:
            report.append("LEARNED ACTIONS (from feedback):")
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
            report.append(f"FEEDBACK HISTORY: {len(self.feedback_history)} entries")
            report.append("")

        report.append("="*70)
        return "\n".join(report)


def main():
    """Main entry point."""
    agent = OrderAgentInteractive("order_train_data.xlsx")
    agent.run_analysis()


if __name__ == "__main__":
    main()
