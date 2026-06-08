# Excel-based Order Analysis Agent Guide

## Overview

The Excel-based Order Analysis Agent creates an Excel file on your desktop with all delayed orders. You can fill in your feedback at your own pace, then run the agent again to process the feedback.

## How It Works

### Step 1: Create the Excel File

Run the agent:
```bash
# Windows
run_agent_excel.bat

# Or manually
python src/order_agent_excel.py
```

Choose option **1** to create the Excel file.

The agent will:
- Analyze your orders and find delayed ones (TAT > 3 days)
- Create an Excel file on your desktop
- Show you the file location

### Step 2: Fill in the Excel File

Open the Excel file on your desktop. You'll see:

**Sheet 1: Orders to Review**
- Source Document Number (order ID)
- Delivery TAT (days)
- Delay Reason (you fill this)
- Actions Taken (you fill this)
- Was Successful? (yes/no/partially) (you fill this)
- Additional Notes (you fill this)

**Sheet 2: Instructions**
- Detailed instructions on how to fill in the feedback
- Examples of what to write

**Sheet 3: Learned Actions**
- Previous successful actions (if any)
- Success rates for each action

### Step 3: Process the Feedback

After filling in the Excel file, run the agent again:
```bash
# Windows
run_agent_excel.bat

# Or manually
python src/order_agent_excel.py
```

Choose option **2** to process the filled Excel file.

The agent will:
- Read the filled Excel file from your desktop
- Process your feedback
- Learn from your actions
- Generate a report

## Example Workflow

```
1. Run agent → Choose option 1
   Agent creates: C:\Users\YourName\Desktop\order_feedback_20260608_233723.xlsx

2. Open Excel file on desktop
   Fill in feedback for each delayed order:
   - Delay Reason: "Stock unavailability at supplier"
   - Actions Taken: "Contacted supplier, offered alternative"
   - Was Successful?: "yes"
   - Additional Notes: "Supplier had backup stock"

3. Save the Excel file

4. Run agent again → Choose option 2
   Agent reads your feedback and learns from it
```

## Benefits

✅ **Handle large numbers** - Process 503 orders without time pressure  
✅ **Offline feedback** - Fill in feedback at your own pace  
✅ **Review and edit** - Check your answers before processing  
✅ **Team collaboration** - Share Excel file with team members  
✅ **Detailed feedback** - Provide thorough feedback for each order  

## Tips for Providing Feedback

1. **Be specific** in your delay reasons
   - Good: "Stock unavailability at supplier warehouse"
   - Bad: "Stock issue"

2. **List all actions** you took, even if they didn't work
   - Good: "Contacted supplier, offered alternative, escalated to management"
   - Bad: "Contacted supplier"

3. **Report success accurately**
   - "yes" - Action was successful
   - "no" - Action was not successful
   - "partially" - Action was partially successful

4. **Add notes** about lessons learned
   - Good: "Supplier had backup stock in different location"
   - Bad: "It worked"

## Files Created

- `order_feedback_*.xlsx` - Excel file on your desktop (you fill this)
- `feedback_history.json` - Learned actions (auto-created)
- `order_analysis_report_*.txt` - Analysis report (auto-created)

## Troubleshooting

**Excel file not created**
- Check if you have write permissions to your Desktop
- Try running the agent as administrator

**Agent can't find the Excel file**
- Make sure the file is on your Desktop
- Check the file name starts with "order_feedback_"
- Don't rename the file

**Feedback not processed**
- Make sure you filled in at least the "Delay Reason" column
- Check that the file is saved (not just open in Excel)
- Run the agent again with option 2

## Version History

- **v0.2.0** - Added Excel-based feedback collection
- **v0.1.0** - Initial release with interactive feedback

## Support

For questions or issues:
- See [ORDER_AGENT_README.md](ORDER_AGENT_README.md)
- See [HOW_TO_RUN.md](HOW_TO_RUN.md)
- See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

**Repository:** https://github.com/k4z0-tech/k4z0
**Last Updated:** 2026-06-08 23:45:00
