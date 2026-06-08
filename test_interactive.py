"""
Test to demonstrate the interactive nature of the agent
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from order_agent_simple import OrderAgent


def test_interactive():
    """Show that the agent waits for human input."""
    print("="*60)
    print("INTERACTIVE AGENT TEST")
    print("="*60)
    print()
    print("The Order Analysis Agent is FULLY INTERACTIVE.")
    print("It will WAIT for human input at each step.")
    print()
    print("When you run the agent:")
    print("1. It will show delayed orders")
    print("2. It will ASK YOU questions about each order")
    print("3. It will WAIT for YOUR answers")
    print("4. It will NOT proceed until you provide input")
    print()
    print("Example questions the agent will ask:")
    print("-" * 60)
    print("1. Why was this order delayed?")
    print("   [Agent waits for your answer]")
    print()
    print("2. What actions did you take to speed up/complete the delivery?")
    print("   [Agent waits for your answer]")
    print()
    print("3. Were your actions successful? (yes/no/partially)")
    print("   [Agent waits for your answer]")
    print()
    print("4. Any additional notes or lessons learned?")
    print("   [Agent waits for your answer]")
    print("-" * 60)
    print()
    print("To run the interactive agent:")
    print("  Windows: run_agent.bat")
    print("  Unix/Mac: ./run_agent.sh")
    print()
    print("="*60)


if __name__ == "__main__":
    test_interactive()
