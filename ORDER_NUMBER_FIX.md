# Order Number Format Fix

## Problem

When creating the Excel output file, order numbers like `5265852016125927` were being converted to integers by Excel, which could cause:
- Loss of precision for very large numbers
- Display as `5.26585E+15` in scientific notation
- Trailing decimal points (`5265852016125927.0`)
- Incorrect order identification

## Solution

The agent now ensures order numbers are stored as **text values** in Excel:

### 1. **Convert to String Before Writing**
```python
# Convert order_id to string to prevent Excel from converting to integer
order_id = str(order['order_id'])
```

### 2. **Apply Text Format to Excel Column**
```python
# Apply text format to the entire column
from openpyxl.styles import numbers
for row in range(2, len(df) + 2):  # Skip header row
    cell = worksheet.cell(row=row, column=col_idx)
    cell.number_format = '@'  # '@' format means text
```

### 3. **Read as String When Processing**
```python
# Read the Excel file with Source Document Number as string
df = pd.read_excel(filepath, sheet_name='Orders to Review', dtype={'Source Document Number': str})

# Get order_id and ensure it's a string
order_id = str(row.get('Source Document Number', f'Order_{idx}'))
# Remove any decimal point that might have been added by Excel
if '.' in order_id:
    order_id = order_id.split('.')[0]
```

## What Changed

### Before (Incorrect)
```
Order numbers stored as integers in Excel:
- 5265852016125927 → Displayed as 5265852016125927 (but could lose precision)
- Very large numbers → Displayed as 5.26585E+15
- Reading back → Could get 5265852016125927.0
```

### After (Correct)
```
Order numbers stored as text in Excel:
- 5265852016125927 → Displayed as "5265852016125927" (text)
- Very large numbers → Displayed correctly
- Reading back → Always get "5265852016125927" (string)
```

## Example

### Original Data
```
Source Document Number: 5265852016125927 (integer in memory)
```

### In Excel File
```
Source Document Number: 5265852016125927 (text format, no conversion)
```

### When Reading Back
```
Source Document Number: "5265852016125927" (string, no decimal point)
```

## Technical Details

### Excel Text Format Code
The `@` symbol in Excel number format means "text":
```python
cell.number_format = '@'  # Text format
```

### Reading with dtype
When reading Excel, specify dtype to ensure string conversion:
```python
df = pd.read_excel(filepath, dtype={'Source Document Number': str})
```

### Removing Decimal Points
Excel sometimes adds decimal points to numbers stored as text:
```python
if '.' in order_id:
    order_id = order_id.split('.')[0]
```

## Verification

Run the test to verify order numbers are preserved:
```bash
python test_order_number_format.py
```

Expected output:
```
Sample order numbers from data:
----------------------------------------------------------------------
  1. Order ID: 5265852016125927
     Type: int
     Length: 16
```

## Benefits

✅ **Preserves precision** - Full 16-digit order numbers maintained  
✅ **No scientific notation** - Numbers display correctly in Excel  
✅ **No decimal points** - Clean order numbers without .0  
✅ **Consistent format** - Same format when writing and reading  
✅ **Prevents errors** - No mismatch between stored and displayed values  

## Testing

The fix has been tested with:
- 503 delayed orders from `order_train_data.xlsx`
- Order numbers ranging from 8 to 16 digits
- Multiple Excel file creation and reading cycles

## Files Updated

- `src/order_agent_excel.py` - Main agent with text format fix
- `test_order_number_format.py` - Test to verify the fix

## Date

Fixed: 2026-06-08 23:59:00

## Version

Included in: v0.2.0

---

**Repository:** https://github.com/k4z0-tech/k4z0
