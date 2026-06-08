# Order ID Fix - Source Document Number

## Issue

The Order Analysis Agent was previously using generic order IDs (`Order ID`, `order_id`, or `Order_{index}`) instead of the actual order identifiers from the Excel file.

## Solution

Updated the agent to use the **"Source Document Number"** column from `order_train_data.xlsx` as the order ID.

## What Changed

### Before (Incorrect)
```python
order_id = row.get('Order ID', row.get('order_id', f'Order_{idx}'))
```
- Used generic column names
- Fell back to index-based IDs (`Order_0`, `Order_1`, etc.)
- Did not reflect actual order identifiers

### After (Correct)
```python
order_id = row.get('Source Document Number', row.get('Order ID', row.get('order_id', f'Order_{idx}')))
```
- Uses "Source Document Number" column first
- Falls back to other column names if needed
- Uses actual order identifiers from the data

## Example

**Before:**
```
Order 1:
   Order ID: Order_0
   Delivery TAT: 74 days
```

**After:**
```
Order 1:
   Order ID: 5265852016125927
   Delivery TAT: 74 days
```

## Verification

Run the verification test:
```bash
python test_order_ids.py
```

Expected output shows actual Source Document Numbers:
```
Sample order IDs (Source Document Numbers):
------------------------------------------------------------
 1. Order ID: 5265852016125927
    Delivery TAT: 74 days

 2. Order ID: 5265832011892576
    Delivery TAT: 75 days
...
```

## Files Updated

- `src/order_agent.py` - Main agent (with emoji support)
- `src/order_agent_simple.py` - Windows-compatible agent

## Testing

Both agents now correctly:
1. Read "Source Document Number" from Excel
2. Use it as the order ID in all operations
3. Display it in delayed orders list
4. Use it in feedback collection
5. Include it in analysis reports

## Impact

- **Better identification**: Orders are now identified by their actual document numbers
- **Easier tracking**: Users can match agent output with their Excel data
- **Accurate feedback**: Feedback is tied to real order identifiers
- **Improved reporting**: Reports use meaningful order IDs

## Date

Fixed: 2026-06-08 20:00:00

## Version

Included in: v0.2.0

---

**Repository:** https://github.com/k4z0-tech/k4z0
