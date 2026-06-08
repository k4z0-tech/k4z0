"""
Quick test for Order Analysis Agent
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from order_agent import OrderAgent


def test_agent():
    """Test the agent with sample data."""
    print("="*60)
    print("TESTING ORDER ANALYSIS AGENT")
    print("="*60)

    # Check if Excel file exists
    if not os.path.exists("order_train_data.xlsx"):
        print("❌ Test file 'order_train_data.xlsx' not found")
        print("   Please ensure the file exists in the project root")
        return False

    try:
        # Initialize agent
        print("\n1. Initializing agent...")
        agent = OrderAgent("order_train_data.xlsx")

        # Test data loading
        print("\n2. Testing data loading...")
        if agent.orders_df.empty:
            print("❌ Failed to load data")
            return False
        print(f"✅ Loaded {len(agent.orders_df)} orders")

        # Test TAT analysis
        print("\n3. Testing TAT analysis...")
        delayed = agent.analyze_delivery_tat()
        print(f"✅ Found {len(delayed)} delayed orders")

        # Test report generation
        print("\n4. Testing report generation...")
        report = agent.generate_report()
        print("✅ Report generated successfully")

        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60)
        return True

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_agent()
    sys.exit(0 if success else 1)
