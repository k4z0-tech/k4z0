# How to Run the Order Analysis Agent

## Important: This is an INTERACTIVE Agent

The Order Analysis Agent is **fully interactive** and requires **human input** at every step. It will:

- **Wait for your answers** to each question
- **Not proceed** until you provide input
- **Learn from your feedback** to help with future orders

## Running the Agent

### Option 1: Use the Batch Script (Windows)

```bash
run_agent.bat
```

### Option 2: Use the Shell Script (Unix/Mac)

```bash
./run_agent.sh
```

### Option 3: Run Manually

**Windows:**
```bash
# Activate virtual environment
.venv\Scripts\activate

# Run the agent
python src/order_agent_simple.py
```

**Unix/Mac:**
```bash
# Activate virtual environment
source .venv/bin/activate

# Run the agent
python src/order_agent_simple.py
```

## What to Expect

### Step 1: Analysis
The agent will analyze your orders and identify delayed ones (TAT > 3 days).

### Step 2: Display
You'll see a list of all delayed orders.

### Step 3: Feedback Collection
For **each delayed order**, the agent will ask you:

1. **Why was this order delayed?**
   - Type your answer and press Enter
   - The agent will WAIT for your response

2. **What actions did you take to speed up/complete the delivery?**
   - List actions separated by commas
   - Press Enter when done
   - The agent will WAIT for your response

3. **Were your actions successful? (yes/no/partially)**
   - Type: yes, no, or partially
   - Press Enter
   - The agent will WAIT for your response

4. **Any additional notes or lessons learned?**
   - Type any additional information
   - Press Enter
   - The agent will WAIT for your response

### Step 4: Learning
The agent will:
- Record your feedback
- Learn from your actions
- Remember successful strategies
- Save everything to `feedback_history.json`

### Step 5: Report
The agent will generate a comprehensive report and save it to a file.

## Example Interaction

```
============================================================
FEEDBACK FOR ORDER: Order_0
============================================================

[TIP] Based on previous experience, here are some suggestions:
   1. Contact supplier (worked 85.0% of the time)
   2. Offer alternative (worked 72.0% of the time)

Please answer the following questions:
------------------------------------------------------------

1. Why was this order delayed?
   Your answer: Stock unavailability at supplier warehouse
   [YOU TYPE THIS AND PRESS ENTER]

2. What actions did you take to speed up/complete the delivery?
   (You can list multiple actions, separated by commas)
   Your answer: Contacted supplier, offered alternative product
   [YOU TYPE THIS AND PRESS ENTER]

3. Were your actions successful? (yes/no/partially)
   Your answer: yes
   [YOU TYPE THIS AND PRESS ENTER]

4. Any additional notes or lessons learned?
   Your answer: Supplier had backup stock in different location
   [YOU TYPE THIS AND PRESS ENTER]

[OK] Feedback recorded successfully!
[STATS] Total feedback entries: 1
[STATS] Learned actions: 2
```

## Key Points

✅ **The agent WAITS for human input** - it will not proceed without your answers

✅ **You control the feedback** - provide accurate information about delays and actions

✅ **The agent learns** - it remembers successful actions for future recommendations

✅ **No auto-answering** - the agent cannot and will not answer for you

## Files Created

After running the agent, you'll find:

- `feedback_history.json` - Your feedback and learned actions
- `order_analysis_report_*.txt` - Detailed analysis report

## Next Time You Run

When you run the agent again:

1. It will show you **learned actions** from previous feedback
2. It will **recommend actions** based on past success rates
3. It will **continue learning** from your new feedback

## Need Help?

- See [ORDER_AGENT_README.md](ORDER_AGENT_README.md) for detailed documentation
- See [QUICK_START.md](QUICK_START.md) for quick reference
- See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for project overview

---

**Remember:** The agent is interactive and requires YOUR input. It will wait for you to answer each question before proceeding.
