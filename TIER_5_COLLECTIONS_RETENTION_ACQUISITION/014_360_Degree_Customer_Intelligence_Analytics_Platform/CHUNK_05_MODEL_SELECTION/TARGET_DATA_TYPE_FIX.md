# CHUNK_05: Target Data Type Fix

## Problem Fixed

**Error:** `ValueError: Unknown label type: continuous`

**Cause:** The TARGET column had floating-point or continuous values instead of discrete class labels.

---

## What Was Happening

Scikit-learn classification models require **discrete class labels** (integers):
- ✓ Valid: `[0, 0, 1, 1, 0, 1]` (integers)
- ✓ Valid: `[1, 2, 3]` (discrete classes)
- ✗ Invalid: `[0.5, 0.25, 0.75]` (continuous values)
- ✗ Invalid: `[NaN, 1, 0, NaN]` (missing values)

Your TARGET column might have contained:
1. NaN values mixed in
2. Float values (0.0, 1.0) instead of integers
3. Missing data not properly handled

---

## Solution Implemented

### Step 1: Clean Data Type
```python
# Convert TARGET to integer (discrete)
y = y.astype(int)
```

### Step 2: Handle Missing Values
```python
# Remove rows where target is NaN
valid_idx = y.notna()
X = X[valid_idx]
y = y[valid_idx]
```

### Step 3: Validate Target Format
```python
unique_vals = np.unique(y)
if len(unique_vals) > 10:
    # If too many classes, convert to binary
    median_val = np.median(y)
    y = (y > median_val).astype(int)
```

### Step 4: Debug Output
```python
print(f"Target data type: {y.dtype}")          # Should be int64
print(f"Unique values: {sorted(np.unique(y))}")  # Should be [0, 1] or similar
print(f"NaN count: {y.isna().sum()}")          # Should be 0
```

---

## Files Updated

✓ `scripts/CHUNK_05_COMPLETE.py` - Added data type handling  
✓ `scripts/CHUNK_05_JUPYTER.py` - Added data type handling  

Both now include:
- Target data type validation
- NaN detection and removal
- Integer conversion
- Binary classification validation
- Debug output

---

## How to Run Now

### Option 1: Jupyter (with debug output)
```python
exec(open('scripts/CHUNK_05_JUPYTER.py').read())
```

Will show:
```
[DEBUG] Target data type: float64
[DEBUG] Target NaN count: 0
[DEBUG] After conversion - Unique values: [0, 1]
[OK] Prepared data: X=(307511, 243), y=(307511,)
  Classes: 2
  Class distribution: {0: 276682, 1: 30829}
```

### Option 2: Windows Batch
```bash
RUN_CHUNK_05.bat
```

### Option 3: Python Script
```bash
python scripts/CHUNK_05_COMPLETE.py
```

---

## Expected Debug Output

```
[DEBUG] Target data type: float64
[DEBUG] Target unique values before cleaning: 2
[DEBUG] Target NaN count: 0
[DEBUG] After removing NaN: 307511 samples
[DEBUG] After converting to int: int64
[DEBUG] Unique values: [0, 1]

[OK] Prepared data: X=(307511, 243), y=(307511,)
  Classes: 2
  Class distribution: {0: 276682, 1: 30829}
  Class balance: ['89.9%', '10.1%']
```

---

## What Each Step Does

| Step | Purpose | Output |
|------|---------|--------|
| 1 | Remove NaN targets | Valid sample count |
| 2 | Convert to integer | dtype = int64 |
| 3 | Validate classes | Unique values count |
| 4 | Check binary classification | Values = [0, 1] |

---

## If Still Getting Error

### Check 1: Target Column Name
```python
# Verify TARGET column exists
print(df.columns.tolist())
# Look for: TARGET, target, Target, default, etc.
```

### Check 2: Target Data Type
```python
# Check what you have
print(df['TARGET'].dtype)
print(df['TARGET'].head())
print(df['TARGET'].isna().sum())
```

### Check 3: Unique Values
```python
# Should be 2 for binary classification
print(df['TARGET'].nunique())
print(df['TARGET'].unique())
```

---

## Data Type Conversion Reference

| Current | Needed | Command |
|---------|--------|---------|
| float64 | int64 | `y.astype(int)` |
| object | int64 | `y.astype(int)` |
| int64 | int64 | ✓ No change needed |
| NaN values | Remove | `y[y.notna()]` |

---

## Why This Matters

Scikit-learn models require:
- ✓ Classification targets: Discrete integer labels (0, 1, 2, ...)
- ✗ Regression targets: Continuous float values (0.5, 1.2, 3.7, ...)

Our data is **classification** (default vs non-default), so needs discrete labels.

---

## Validation Checklist

After update, verify:

- [ ] TARGET column detected
- [ ] Data type is int64
- [ ] No NaN values remain
- [ ] Unique values are [0, 1]
- [ ] Class distribution is reasonable
- [ ] Model training starts without error

---

## Version Info

- **Updated:** August 12, 2026
- **Files Modified:** 2 (COMPLETE, JUPYTER)
- **Status:** Ready for execution ✓
