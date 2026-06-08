# Order Analysis Agent

An intelligent agent that analyzes order delivery delays, gathers user feedback, and learns from past actions to provide better guidance over time.

## Features

- 📊 **Automated Analysis**: Analyzes Delivery TAT from Excel files
- 🚨 **Delay Detection**: Identifies orders with TAT > 3 days
- 📝 **Feedback Collection**: Gathers detailed feedback for each delayed order
- 🧠 **Learning System**: Remembers successful actions and provides recommendations
- 📈 **Reporting**: Generates comprehensive analysis reports
- 💾 **Persistence**: Saves feedback history for future reference

## How It Works

1. **Load Data**: Reads order data from `order_train_data.xlsx`
2. **Analyze TAT**: Identifies orders with Delivery TAT > 3 days
3. **Display Delays**: Shows delayed orders to the user
4. **Gather Feedback**: Asks user about delay reasons and actions taken
5. **Learn & Remember**: Stores feedback and learns successful strategies
6. **Provide Guidance**: Uses learned actions to recommend solutions for future orders

## Usage

### Running the Agent

```bash
python src/order_agent.py
```

### What to Expect

The agent will:

1. **Analyze your orders** and identify delayed ones
2. **Display a list** of all delayed orders
3. **Ask for feedback** for each delayed order:
   - Why was the order delayed?
   - What actions did you take?
   - Were the actions successful?
   - Any additional notes?
4. **Learn from your feedback** and remember successful strategies
5. **Generate a report** with analysis and recommendations

### Example Interaction

```
🚨 DELAYED ORDERS ALERT
============================================================
Total delayed orders: 5
Threshold: > 3 days Delivery TAT
============================================================

📦 Order 1:
   Order ID: ORD-001
   Delivery TAT: 5.2 days
   Status: DELAYED

💡 GUIDANCE FOR ORDER ORD-001:
============================================================
Based on previous feedback, here are recommended actions:

1. Contacted supplier
   Success rate: 85.0%
   Used 12 times

2. Escalated to management
   Success rate: 72.0%
   Used 8 times
============================================================

📝 FEEDBACK FOR ORDER: ORD-001
============================================================

1. Why was this order delayed?
   Your answer: Stock unavailability at supplier warehouse

2. What actions did you take to speed up/complete the delivery?
   Your answer: Contacted supplier, offered alternative product

3. Were your actions successful? (yes/no/partially): yes

4. Any additional notes or lessons learned?
   Your answer: Supplier had backup stock in different location

✅ Feedback recorded successfully!
```

## Feedback System

The agent learns from your feedback:

- **Successful actions** are remembered and recommended for similar situations
- **Success rates** are calculated based on your feedback
- **Similar situations** are identified to provide relevant guidance
- **Feedback history** is preserved across sessions

## Files

- `src/order_agent.py` - Main agent code
- `src/config.py` - Configuration settings
- `feedback_history.json` - Stored feedback and learned actions (auto-generated)
- `order_analysis_report_*.txt` - Generated analysis reports (auto-generated)

## Requirements

- Python 3.8+
- pandas
- openpyxl (for reading Excel files)

Install dependencies:
```bash
pip install pandas openpyxl
```

## Configuration

Edit `src/config.py` to customize:

- `DEFAULT_TAT_THRESHOLD_DAYS` - Delay threshold (default: 3 days)
- `DATA_FILE` - Path to Excel file
- `COLUMN_MAPPINGS` - Column name variations to look for

## Learning Mechanism

The agent uses a simple but effective learning system:

1. **Action Tracking**: Records every action you take
2. **Success Rate**: Calculates success percentage for each action
3. **Context Matching**: Links actions to delay reasons
4. **Recommendation Engine**: Suggests actions with highest success rates

## Example Feedback Flow

```
Order delayed → Gather feedback → Learn actions → Provide guidance
     ↓              ↓                ↓                ↓
  ORD-001      "Stock issue"    "Contact supplier"  "85% success"
     ↓              ↓                ↓                ↓
  ORD-002      "Stock issue"    → Recommends: "Contact supplier"
```

## Tips for Effective Use

1. **Be specific** in your feedback - detailed reasons help the agent learn better
2. **List all actions** you took, even if they didn't work
3. **Report success accurately** - this improves future recommendations
4. **Add notes** about lessons learned - the agent remembers these
5. **Review reports** to see patterns in delays and successful solutions

## Troubleshooting

**No Excel file found**
- Ensure `order_train_data.xlsx` is in the project root directory
- Check the file name matches the configuration

**Column not found**
- The agent looks for columns containing "delivery" and "tat" (case-insensitive)
- Update `COLUMN_MAPPINGS` in `config.py` if your columns have different names

**No delayed orders found**
- All orders may have TAT ≤ 3 days
- Adjust `DEFAULT_TAT_THRESHOLD_DAYS` in `config.py` if needed

## Future Enhancements

- [ ] Machine learning for pattern recognition
- [ ] Integration with order management systems
- [ ] Automated notifications for new delays
- [ ] Dashboard for visualizing delay patterns
- [ ] Export to various formats (CSV, PDF)
