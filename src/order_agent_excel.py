"""
Order Analysis Agent - Excel-based Feedback
Creates Excel file for users to fill in feedback, then reads and processes it.
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json
import os
import sys


class OrderAgentExcel:
    """
    Agent that creates Excel file for feedback collection and processes filled responses.
    """

    def __init__(self, data_file: str = "order_train_data.xlsx"):
        self.data_file = data_file
        self.orders_df = None
        self.delayed_orders = []
        self.feedback_history = []
        self.learned_actions = {}
        self.feedback_file = "feedback_history.json"
        self.feedback_excel_file = None
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

    def get_similar_actions(self) -> List[Dict[str, Any]]:
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

    def create_feedback_excel(self) -> str:
        """Create Excel file with delayed orders for user feedback."""
        if not self.delayed_orders:
            print("[ERROR] No delayed orders to create feedback file")
            return None

        # Get desktop path
        desktop_path = self.get_desktop_path()
        if not desktop_path:
            print("[ERROR] Could not find desktop path")
            return None

        # Check for existing feedback files
        existing_files = []
        for file in os.listdir(desktop_path):
            if file.startswith('order_feedback_') and file.endswith('.xlsx'):
                existing_files.append(file)

        # Create filename with timestamp and version
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        if existing_files:
            # Add version number to avoid confusion
            version = len(existing_files) + 1
            filename = f"order_feedback_{timestamp}_v{version}.xlsx"
        else:
            filename = f"order_feedback_{timestamp}.xlsx"

        filepath = os.path.join(desktop_path, filename)

        # Prepare data for Excel
        excel_data = []
        for i, order in enumerate(self.delayed_orders, 1):
            # Convert order_id to string to prevent Excel from converting to integer
            order_id = str(order['order_id'])
            row = {
                'Row Number': i,
                'Source Document Number': order_id,
                'Delivery TAT (days)': order['delivery_tat'],
                'Delay Reason': '',  # User fills this
                'Actions Taken': '',  # User fills this
                'Was Successful? (yes/no/partially)': '',  # User fills this
                'Additional Notes': ''  # User fills this
            }
            excel_data.append(row)

        # Create DataFrame
        df = pd.DataFrame(excel_data)

        # Convert Source Document Number column to string type to preserve leading zeros and prevent integer conversion
        df['Source Document Number'] = df['Source Document Number'].astype(str)

        # Add instructions sheet
        instructions_data = {
            'Instructions': [
                'Order Feedback Form',
                '',
                'Please fill in the following columns for each delayed order:',
                '',
                '1. Delay Reason: Why was this order delayed?',
                '   Examples: Stock unavailability, Logistics delay, Customs clearance, etc.',
                '',
                '2. Actions Taken: What actions did you take to speed up/complete the delivery?',
                '   List multiple actions separated by commas',
                '   Examples: Contacted supplier, Offered alternative, Escalated to management',
                '',
                '3. Was Successful? (yes/no/partially): Were your actions successful?',
                '   Type: yes, no, or partially',
                '',
                '4. Additional Notes: Any additional notes or lessons learned?',
                '',
                'Tips:',
                '- Be specific in your feedback',
                '- List all actions you took, even if they didn\'t work',
                '- Report success accurately to improve future recommendations',
                '',
                f'Total delayed orders: {len(self.delayed_orders)}',
                f'Average TAT: {sum(o["delivery_tat"] for o in self.delayed_orders)/len(self.delayed_orders):.1f} days',
                '',
                'After filling in the feedback, save this file and run the agent again to process it.'
            ]
        }
        instructions_df = pd.DataFrame(instructions_data)

        # Add learned actions sheet if available
        similar_actions = self.get_similar_actions()
        if similar_actions:
            actions_data = {
                'Action': [a['action'] for a in similar_actions],
                'Success Rate (%)': [a['success_rate'] for a in similar_actions],
                'Times Used': [a['total_uses'] for a in similar_actions]
            }
            actions_df = pd.DataFrame(actions_data)
        else:
            actions_df = pd.DataFrame({'Note': ['No previous feedback recorded yet']})

        # Write to Excel with multiple sheets
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Orders to Review', index=False)

            # Format Source Document Number column as text to prevent integer conversion
            workbook = writer.book
            worksheet = writer.sheets['Orders to Review']

            # Find the column index for Source Document Number
            col_idx = None
            for col_num, value in enumerate(df.columns, 1):
                if value == 'Source Document Number':
                    col_idx = col_num
                    break

            if col_idx:
                # Apply text format to the entire column
                from openpyxl.styles import numbers
                for row in range(2, len(df) + 2):  # Skip header row
                    cell = worksheet.cell(row=row, column=col_idx)
                    cell.number_format = '@'  # '@' format means text

            instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
            actions_df.to_excel(writer, sheet_name='Learned Actions', index=False)

        print(f"\n[OK] Feedback Excel file created!")
        print(f"[LOCATION] {filepath}")
        print(f"\n[NEXT STEPS]")
        print(f"1. Open the Excel file")
        print(f"2. Fill in the 'Orders to Review' sheet")
        print(f"3. Save the file")
        print(f"4. Run this agent again to process the feedback")

        self.feedback_excel_file = filepath
        return filepath

    def get_desktop_path(self) -> str:
        """Get the desktop path for the current user."""
        # Try common desktop locations
        possible_paths = [
            os.path.join(os.path.expanduser('~'), 'Desktop'),
            os.path.join(os.path.expanduser('~'), 'OneDrive', 'Desktop'),
            os.path.join(os.path.expanduser('~'), 'OneDrive', 'שולחן העבודה'),  # Hebrew
            os.path.join(os.path.expanduser('~'), 'שולחן העבודה'),  # Hebrew
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path

        # If none found, try to create Desktop folder
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        try:
            os.makedirs(desktop_path, exist_ok=True)
            return desktop_path
        except:
            pass

        return None

    def read_feedback_excel(self, filepath: str = None) -> List[Dict[str, Any]]:
        """Read feedback from filled Excel file."""
        if filepath is None:
            # Find feedback files on desktop
            desktop_path = self.get_desktop_path()
            if not desktop_path:
                print("[ERROR] Could not find desktop path")
                return []

            # Look for feedback files
            feedback_files = []
            for file in os.listdir(desktop_path):
                if file.startswith('order_feedback_') and file.endswith('.xlsx'):
                    # Get file modification time
                    file_path = os.path.join(desktop_path, file)
                    mod_time = os.path.getmtime(file_path)
                    feedback_files.append((file, mod_time))

            if not feedback_files:
                print("[ERROR] No feedback Excel files found on desktop")
                print("[INFO] Please run the agent first to create the feedback file")
                return []

            # Sort by modification time (most recent first)
            feedback_files.sort(key=lambda x: x[1], reverse=True)

            # Show available files
            print(f"\n[INFO] Found {len(feedback_files)} feedback file(s) on desktop:")
            print("-" * 70)
            for i, (file, mod_time) in enumerate(feedback_files, 1):
                # Convert timestamp to readable format
                from datetime import datetime
                mod_datetime = datetime.fromtimestamp(mod_time)
                print(f"  {i}. {file}")
                print(f"     Last modified: {mod_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

            # Ask user which file to use
            if len(feedback_files) > 1:
                print("\n" + "="*70)
                print("MULTIPLE FEEDBACK FILES FOUND")
                print("="*70)
                print("Options:")
                print("  1. Use most recent file (recommended)")
                print("  2. Choose specific file")
                print("  3. Cancel")

                choice = input("\nYour choice (1-3): ").strip()

                if choice == '3':
                    print("\n[INFO] Operation cancelled")
                    return []

                if choice == '2':
                    # Let user choose specific file
                    print(f"\nEnter file number (1-{len(feedback_files)}): ")
                    try:
                        file_num = int(input().strip())
                        if 1 <= file_num <= len(feedback_files):
                            selected_file = feedback_files[file_num - 1][0]
                        else:
                            print("[ERROR] Invalid file number, using most recent")
                            selected_file = feedback_files[0][0]
                    except ValueError:
                        print("[ERROR] Invalid input, using most recent")
                        selected_file = feedback_files[0][0]
                else:
                    # Use most recent
                    selected_file = feedback_files[0][0]
            else:
                # Only one file, use it
                selected_file = feedback_files[0][0]

            filepath = os.path.join(desktop_path, selected_file)
            print(f"\n[INFO] Using feedback file: {filepath}")

        try:
            # Read the Excel file
            df = pd.read_excel(filepath, sheet_name='Orders to Review', dtype={'Source Document Number': str})
            print(f"[OK] Read {len(df)} rows from feedback file")

            # Process each row
            feedback_list = []
            for idx, row in df.iterrows():
                # Check if user filled in at least the delay reason
                delay_reason = str(row.get('Delay Reason', '')).strip()
                if not delay_reason or delay_reason == 'nan':
                    continue  # Skip rows without feedback

                # Get order_id and ensure it's a string
                order_id = str(row.get('Source Document Number', f'Order_{idx}'))
                # Remove any decimal point that might have been added by Excel
                if '.' in order_id:
                    order_id = order_id.split('.')[0]

                feedback = {
                    'order_id': order_id,
                    'timestamp': datetime.now().isoformat(),
                    'delay_reason': delay_reason,
                    'actions_taken': [a.strip() for a in str(row.get('Actions Taken', '')).split(',')],
                    'success': str(row.get('Was Successful? (yes/no/partially)', '')).strip().lower(),
                    'additional_notes': str(row.get('Additional Notes', '')).strip()
                }
                feedback_list.append(feedback)

            print(f"[OK] Processed {len(feedback_list)} feedback entries")
            return feedback_list

        except Exception as e:
            print(f"[ERROR] Error reading feedback file: {e}")
            return []

    def process_feedback(self, feedback_list: List[Dict[str, Any]]):
        """Process and store feedback, update learned actions."""
        for feedback in feedback_list:
            # Store feedback
            self.feedback_history.append(feedback)

            # Update learned actions
            for action in feedback['actions_taken']:
                if action and action != 'nan':
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

        print(f"\n[OK] Feedback processed successfully!")
        print(f"[STATS] Total feedback entries: {len(self.feedback_history)}")
        print(f"[STATS] Learned actions: {len(self.learned_actions)}")

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

    def run_analysis(self):
        """Main method to run the complete analysis workflow."""
        print("\n" + "="*70)
        print("ORDER ANALYSIS AGENT - EXCEL FEEDBACK MODE")
        print("="*70)
        print("This agent creates an Excel file for you to fill in feedback.")
        print("="*70 + "\n")

        # Step 1: Analyze delivery TAT
        print("[STEP 1] Analyzing Delivery TAT...")
        delayed_orders = self.analyze_delivery_tat()

        if not delayed_orders:
            print("\n[OK] All orders are within acceptable delivery times!")
            return

        # Step 2: Display summary
        print("\n[STEP 2] Displaying summary...")
        print(f"\nTotal delayed orders: {len(self.delayed_orders)}")

        if self.delayed_orders:
            tat_values = [o['delivery_tat'] for o in self.delayed_orders]
            print(f"Average TAT: {sum(tat_values)/len(tat_values):.1f} days")
            print(f"Min TAT: {min(tat_values)} days")
            print(f"Max TAT: {max(tat_values)} days")

        # Step 3: Ask user what to do
        print("\n[STEP 3] Choose action:")
        print("  1. Create Excel file with delayed orders (for feedback)")
        print("  2. Process filled Excel file (read feedback)")
        print("  3. Create Excel and process immediately (skip waiting)")
        print("  4. Exit")

        choice = input("\nYour choice (1-4): ").strip()

        if choice == '4':
            print("\nExiting...")
            return

        elif choice == '1':
            # Create Excel file
            print("\n[CREATING] Excel file with delayed orders...")
            filepath = self.create_feedback_excel()
            if filepath:
                print(f"\n[DONE] Excel file created on your desktop!")
                print(f"[FILE] {filepath}")
                print(f"\n[NEXT] Fill in the feedback in the Excel file and run this agent again with option 2.")

        elif choice == '2':
            # Process filled Excel file
            print("\n[READING] Looking for filled Excel file on desktop...")
            feedback_list = self.read_feedback_excel()

            if feedback_list:
                print(f"\n[PROCESSING] {len(feedback_list)} feedback entries...")
                self.process_feedback(feedback_list)

                # Generate report
                print("\n[GENERATING] Analysis report...")
                report = self.generate_report()
                print(report)

                # Save report
                report_file = f"order_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(report_file, 'w') as f:
                    f.write(report)
                print(f"\n[SAVED] Report saved to: {report_file}")
            else:
                print("\n[INFO] No feedback found to process.")
                print("[INFO] Please fill in the Excel file first.")

        elif choice == '3':
            # Create Excel and process immediately (for testing)
            print("\n[CREATING] Excel file with delayed orders...")
            filepath = self.create_feedback_excel()

            if filepath:
                print(f"\n[INFO] Excel file created: {filepath}")
                print("[INFO] For testing, we'll process it immediately.")
                print("[NOTE] In real use, you would fill in the Excel file first.")

                # For demo purposes, we'll create a sample filled file
                print("\n[DEMO] Creating sample filled file for testing...")
                self.create_sample_filled_file(filepath)

                # Process the sample file
                print("\n[PROCESSING] Sample feedback...")
                feedback_list = self.read_feedback_excel(filepath)

                if feedback_list:
                    self.process_feedback(feedback_list)

                    # Generate report
                    print("\n[GENERATING] Analysis report...")
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

    def create_sample_filled_file(self, filepath: str):
        """Create a sample filled file for testing purposes."""
        try:
            # Read the original file
            df = pd.read_excel(filepath, sheet_name='Orders to Review')

            # Fill in sample data for first 5 orders
            sample_reasons = [
                'Stock unavailability at supplier warehouse',
                'Logistics delay due to weather conditions',
                'Customs clearance issues',
                'Quality check failed - needed replacement',
                'Customer requested delay for personal reasons'
            ]

            sample_actions = [
                'Contacted supplier, offered alternative product',
                'Changed shipping method, expedited processing',
                'Escalated to management, contacted customs broker',
                'Arranged pickup, provided replacement product',
                'Extended delivery window, offered discount'
            ]

            sample_success = ['yes', 'partially', 'yes', 'yes', 'no']

            sample_notes = [
                'Supplier had backup stock in different location',
                'Air freight was faster but more expensive',
                'Customs broker helped expedite clearance',
                'Customer was happy with the replacement',
                'Customer decided to cancel the order'
            ]

            # Fill in sample data
            for i in range(min(5, len(df))):
                df.at[i, 'Delay Reason'] = sample_reasons[i]
                df.at[i, 'Actions Taken'] = sample_actions[i]
                df.at[i, 'Was Successful? (yes/no/partially)'] = sample_success[i]
                df.at[i, 'Additional Notes'] = sample_notes[i]

            # Save the filled file
            df.to_excel(filepath, sheet_name='Orders to Review', index=False)
            print(f"[OK] Sample filled file created for testing")

        except Exception as e:
            print(f"[WARNING] Could not create sample filled file: {e}")


def main():
    """Main entry point."""
    agent = OrderAgentExcel("order_train_data.xlsx")
    agent.run_analysis()


if __name__ == "__main__":
    main()
