"""
Demo script for Order Analysis Agent
Shows how the agent works without interactive input
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from order_agent_simple import OrderAgent


def demo():
    """Run a demonstration of the agent."""
    print("="*80)
    print("ORDER ANALYSIS AGENT - DEMONSTRATION")
    print("="*80)

    # Initialize agent
    print("\n[1] Initializing agent...")
    agent = OrderAgent("order_train_data.xlsx")

    # Analyze delivery TAT
    print("\n[2] Analyzing Delivery TAT...")
    delayed = agent.analyze_delivery_tat()

    # Display results
    print("\n[3] Analysis Results:")
    print(f"   Total orders: {len(agent.orders_df)}")
    print(f"   Delayed orders (>3 days): {len(delayed)}")
    if len(agent.orders_df) > 0:
        print(f"   Delay rate: {len(delayed)/len(agent.orders_df)*100:.1f}%")

    # Show sample delayed orders
    if delayed:
        print("\n[4] Sample Delayed Orders:")
        for i, order in enumerate(delayed[:5], 1):
            print(f"   {i}. Order ID: {order['order_id']}")
            print(f"      Delivery TAT: {order['delivery_tat']} days")

    # Show learned actions
    print("\n[5] Learned Actions:")
    if agent.learned_actions:
        sorted_actions = sorted(
            agent.learned_actions.items(),
            key=lambda x: x[1]['success_rate'],
            reverse=True
        )
        for i, (action, data) in enumerate(sorted_actions[:5], 1):
            print(f"   {i}. {action}")
            print(f"      Success rate: {data['success_rate']}%")
    else:
        print("   No feedback recorded yet")
        print("   Run the interactive agent to provide feedback")

    # Generate report
    print("\n[6] Generating report...")
    report = agent.generate_report()

    # Save demo report
    demo_report_file = "demo_analysis_report.txt"
    with open(demo_report_file, 'w') as f:
        f.write(report)
    print(f"   Report saved to: {demo_report_file}")

    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE")
    print("="*80)
    print("\nTo run the full interactive agent:")
    print("  Windows: run_agent.bat")
    print("  Unix/Mac: ./run_agent.sh")
    print("="*80 + "\n")


if __name__ == "__main__":
    demo()
