# Quick Start Guide

## Order Analysis Agent

### Run the Agent

**Windows:**
```bash
run_agent.bat
```

**Unix/Mac:**
```bash
./run_agent.sh
```

**Manual:**
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/Mac

# Run agent
python src/order_agent_simple.py
```

### Run Demo (No Interaction)

```bash
python demo_agent.py
```

## What the Agent Does

1. **Analyzes** your order data from `order_train_data.xlsx`
2. **Identifies** orders with Delivery TAT > 3 days
3. **Asks** you why each order was delayed
4. **Records** what actions you took
5. **Learns** from your feedback
6. **Remembers** successful actions for future use
7. **Provides** guidance based on past experience

## Example Workflow

```
Agent: "Found 503 delayed orders"

Agent: "Why was Order_0 delayed?"
You: "Stock unavailability"

Agent: "What actions did you take?"
You: "Contacted supplier, offered alternative"

Agent: "Were actions successful?"
You: "yes"

Agent: "Feedback recorded. I'll remember this."
```

## Next Time

When you encounter similar delays:
```
Agent: "Based on previous feedback, try:
1. Contact supplier (85% success rate)
2. Offer alternative (72% success rate)"
```

## Files

- `order_train_data.xlsx` - Your order data
- `feedback_history.json` - Learned actions (auto-created)
- `*_report.txt` - Analysis reports (auto-created)

## Version History

See [CHANGELOG.md](CHANGELOG.md) for all changes with timestamps.

## Need Help?

- [ORDER_AGENT_README.md](ORDER_AGENT_README.md) - Detailed documentation
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
