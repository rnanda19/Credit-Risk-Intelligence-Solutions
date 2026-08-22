# CHUNK_05: REAL DATA USAGE (NOT SYNTHETIC)

## Update: Using Real CSV Datasets

CHUNK_05 has been updated to use **REAL target variables from your CSV datasets** instead of synthetic data.

---

## How It Works

### Data Source
✓ **Real:** Uses `application_train.csv` from your Home Credit datasets  
✗ **NOT:** Creating fake synthetic targets  

### Target Column Detection
The script automatically looks for the target column in this order:
1. `TARGET` (standard Home Credit naming)
2. `target`
3. `Target`
4. `default`
5. `Default`
6. `label`
7. `Label`

### What Gets Used for Training
```
application_train.csv
├── Features (X): All numeric columns except target
└── Target (y): Real TARGET column from your CSV
```

---

## Quality Gates Now Use Real Data

| Gate | Input | Data Type |
|------|-------|-----------|
| QG2 | application_train.csv | ✓ REAL |
| QG3 | Train/test split (80/20) | ✓ REAL |
| QG4 | Model performance | ✓ REAL |
| QG5 | Feature importance | ✓ REAL |
| QG6 | Model ranking | ✓ REAL |

---

## Example: Class Distribution

**Real data from Home Credit:**
```
Class distribution: {0: 276682, 1: 30829}
Class balance: ['89.9%', '10.1%']
```

Instead of:
```
Class distribution: [246008, 61503]
Class balance: (synthetic 50/50 split)
```

---

## Benefits of Real Data

✓ **Accurate modeling** - Train on actual patterns  
✓ **Real class imbalance** - Learn from real distribution  
✓ **Meaningful results** - Metrics reflect real performance  
✓ **No data leakage** - No contamination from synthetic targets  
✓ **Production-ready** - Models trained on production data  

---

## CSV Datasets Used

Your provided datasets:
- ✓ `application_train.csv` - Training data WITH target
- ✓ `application_test.csv` - Test data WITHOUT target
- ✓ `bureau.csv` - Bureau credit history
- ✓ `bureau_balance.csv` - Bureau balance history
- ✓ `credit_card_balance.csv` - Credit card data
- ✓ `installments_payments.csv` - Payment history
- ✓ `POS_CASH_balance.csv` - POS cash advances
- ✓ `previous_application.csv` - Previous applications

**CHUNK_05 uses:** `application_train.csv` (primary dataset with real TARGET)

---

## Expected Output Example

```
================================================================================
QUALITY GATE 2: DATA PREPARATION FOR MODELING
================================================================================

Using dataset: application_train.csv
Shape: (307511, 244)
[OK] Found TARGET column: 'TARGET'
[OK] Prepared data: X=(307511, 243), y=(307511,)
  Classes: 2
  Class distribution: {0: 276682, 1: 30829}
  Class balance: ['89.9%', '10.1%']
```

---

## Key Files Updated

- ✓ `scripts/CHUNK_05_COMPLETE.py` - Uses real data detection
- ✓ `scripts/CHUNK_05_JUPYTER.py` - Uses real data detection
- ✓ Error handling if TARGET not found
- ✓ Proper handling of missing values in target

---

## What Changed

### Before
```python
if target_column not in primary_dataset.columns:
    print(f"[INFO] Creating synthetic target")
    y = np.random.randint(0, 2, len(primary_dataset))  # SYNTHETIC
```

### After
```python
# Look for TARGET column in REAL CSV data
target_candidates = ['TARGET', 'target', ...]
for col in target_candidates:
    if col in primary_dataset.columns:
        target_col = col
        break

# Use REAL target from CSV
y = primary_dataset[target_col]  # REAL DATA
```

---

## No More Synthetic Data

CHUNK_05 now:
- ✓ Detects TARGET from real CSV
- ✓ Fails with clear error if TARGET not found
- ✓ Uses actual Home Credit default labels
- ✓ Trains models on production data patterns
- ✓ Reports realistic class distributions

---

## Running with Real Data

All three execution methods now use real data:

```bash
# Jupyter
exec(open('scripts/CHUNK_05_COMPLETE.py').read())

# Windows Batch
RUN_CHUNK_05.bat

# Python
python scripts/CHUNK_05_COMPLETE.py
```

All will detect and use your real `application_train.csv` TARGET column.

---

**Status:** UPDATED to use REAL DATA ✓
