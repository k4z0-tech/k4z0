# How the Agent Handles Multiple Feedback Files

## Problem

If you run the agent multiple times, you'll have multiple Excel files on your desktop:
- `order_feedback_20260608_233723.xlsx`
- `order_feedback_20260608_233757.xlsx`
- `order_feedback_20260608_233956_v3.xlsx`

How does the agent know which one to read?

## Solution

The agent has been improved to handle multiple files intelligently:

### 1. **Automatic Version Numbers**

When you create multiple feedback files, the agent automatically adds version numbers:
- First file: `order_feedback_20260608_233723.xlsx`
- Second file: `order_feedback_20260608_233757.xlsx`
- Third file: `order_feedback_20260608_233956_v3.xlsx`

This makes it easy to identify which file is newer.

### 2. **File Selection Menu**

When you run the agent to process feedback (option 2), it will:

1. **Show all available files** with their modification timestamps
2. **Let you choose** which file to use
3. **Default to most recent** if you don't choose

**Example output:**
```
[INFO] Found 3 feedback file(s) on desktop:
----------------------------------------------------------------------
  1. order_feedback_20260608_233723.xlsx
     Last modified: 2026-06-08 23:37:23
  2. order_feedback_20260608_233757.xlsx
     Last modified: 2026-06-08 23:37:57
  3. order_feedback_20260608_233956_v3.xlsx
     Last modified: 2026-06-08 23:39:56

======================================================================
MULTIPLE FEEDBACK FILES FOUND
======================================================================
Options:
  1. Use most recent file (recommended)
  2. Choose specific file
  3. Cancel

Your choice (1-3):
```

### 3. **Recommended Workflow**

**Option A: Use Most Recent (Recommended)**
- Just press **1** or **Enter** when prompted
- Agent uses the most recent file automatically
- Best for most users

**Option B: Choose Specific File**
- Press **2** when prompted
- Enter the file number (1, 2, 3, etc.)
- Best when you want to use an older file

**Option C: Cancel**
- Press **3** to cancel
- Agent exits without processing

## Best Practices

### ✅ **Do This:**

1. **Fill in feedback immediately** after creating the Excel file
2. **Save the file** before running the agent again
3. **Use option 1 (most recent)** unless you have a specific reason
4. **Delete old files** you no longer need (optional)

### ❌ **Avoid This:**

1. **Don't rename** the feedback files
2. **Don't move** the files to different folders
3. **Don't create multiple files** without filling in feedback first
4. **Don't open the file** in Excel while the agent is reading it

## Example Workflow

### Step 1: Create Feedback File
```bash
run_agent_excel.bat
# Choose option 1
# Agent creates: order_feedback_20260608_233723.xlsx
```

### Step 2: Fill in Feedback
- Open the Excel file on your desktop
- Fill in the "Orders to Review" sheet
- Save the file

### Step 3: Process Feedback
```bash
run_agent_excel.bat
# Choose option 2
# Agent shows available files
# Choose option 1 (most recent) or specific file
# Agent processes your feedback
```

### Step 4: Repeat (Optional)
If you need to provide more feedback:
```bash
run_agent_excel.bat
# Choose option 1 to create new file
# Fill in feedback
# Choose option 2 to process
```

## Troubleshooting

### **"No feedback Excel files found on desktop"**
- Make sure the file is on your Desktop (not in a subfolder)
- Check the file name starts with "order_feedback_"
- Don't rename the file

### **Agent uses wrong file**
- Use option 2 to choose specific file
- Check the "Last modified" timestamp
- Delete old files you don't need

### **File is locked by Excel**
- Close the Excel file before running the agent
- Save the file first
- Wait a few seconds after saving

### **Multiple files with same timestamp**
- This shouldn't happen with version numbers
- If it does, use option 2 to choose specific file
- Delete duplicate files

## Technical Details

### How the Agent Finds Files

1. **Searches Desktop** for files matching `order_feedback_*.xlsx`
2. **Sorts by modification time** (most recent first)
3. **Shows all files** with timestamps
4. **Lets user choose** or defaults to most recent

### File Naming Convention

```
order_feedback_YYYYMMDD_HHMMSS[_vN].xlsx

Examples:
- order_feedback_20260608_233723.xlsx (first file)
- order_feedback_20260608_233757.xlsx (second file)
- order_feedback_20260608_233956_v3.xlsx (third file, with version)
```

### Why Version Numbers?

- **Avoids confusion** when multiple files exist
- **Makes it easy** to identify newer files
- **Prevents accidental** overwrites
- **Helps track** your feedback history

## Summary

The agent intelligently handles multiple feedback files by:

✅ **Adding version numbers** to new files  
✅ **Showing all available files** with timestamps  
✅ **Letting you choose** which file to use  
✅ **Defaulting to most recent** for convenience  
✅ **Providing clear instructions** at each step  

You can safely run the agent multiple times without worrying about file conflicts!

---

**Repository:** https://github.com/k4z0-tech/k4z0
**Last Updated:** 2026-06-08 23:55:00
