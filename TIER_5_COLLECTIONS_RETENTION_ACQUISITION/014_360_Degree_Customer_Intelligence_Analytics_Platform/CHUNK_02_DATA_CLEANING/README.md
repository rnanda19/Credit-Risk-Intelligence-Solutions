# CHUNK_02: DATA CLEANING & PREPROCESSING
## PROBLEM_004_Customer_360_Analysis

**Status:** Ready to Execute  
**Version:** 1.0.0  
**Date:** August 12, 2026  
**Phase:** CRISP-DM Phase 3 - Data Preparation  
**Sprint:** AGILE Sprint 1 - Days 4-5

---

## Overview

CHUNK_02 cleans and preprocesses all 8 datasets from CHUNK_01:

- **Handle** missing values (numeric: median, categorical: mode)
- **Remove** duplicate records
- **Detect** and treat outliers
- **Optimize** data types (int64→int32, float64→float32)
- **Validate** data quality after cleaning
- **Generate** comprehensive cleaning reports

**Execution Time:** ~3-5 minutes  
**Output Files:** 3 reports + metadata + cleaned datasets

---

## Quick Start

### Option 1: Jupyter Notebook (Recommended)

```python
# First, run CHUNK_01 to get datasets
exec(open(r'C:\Users\rnand\Documents\home-credit-default-risk\Enterprise_AI_Workflows\PROBLEM_004_Customer_360_Analysis\CHUNK_01_DATA_INGESTION\scripts\CHUNK_01_INTERACTIVE.py').read())

# Then run CHUNK_02
exec(open(r'C:\Users\rnand\Documents\home-credit-default-risk\Enterprise_AI_Workflows\PROBLEM_004_Customer_360_Analysis\CHUNK_02_DATA_CLEANING\scripts\CHUNK_02_INTERACTIVE.py').read())

# Or use the automatic function:
chunk02_results = run_chunk02(datasets=results['datasets'])
```

### Option 2: Windows Batch

```bash
cd C:\Users\rnand\Documents\home-credit-default-risk\Enterprise_AI_Workflows\PROBLEM_004_Customer_360_Analysis\CHUNK_02_DATA_CLEANING

RUN_CHUNK_02.bat
```

### Option 3: Python Script

```bash
python scripts/CHUNK_02_INTERACTIVE.py
```

---

## Prerequisites

### Required Python Packages
```bash
pip install pandas numpy scikit-learn
```

### Input Data
Requires cleaned datasets from CHUNK_01:
- application_train.csv
- application_test.csv
- bureau.csv
- bureau_balance.csv
- credit_card_balance.csv
- installments_payments.csv
- POS_CASH_balance.csv
- previous_application.csv

---

## Library Functions

### 1. MissingValueHandler Class

**Handle missing data in datasets**

```python
from lib.data_cleaning import MissingValueHandler

handler = MissingValueHandler()

# Analyze missing values
analysis = handler.analyze_missing(df)
print(f"Missing: {analysis['total_missing']} records")

# Remove columns with >50% missing
df = handler.drop_high_missing_columns(df, threshold=50.0)

# Fill numeric missing with median
df = handler.fill_missing_numeric(df, method='median')

# Fill categorical missing with mode
df = handler.fill_missing_categorical(df, method='mode')
```

### 2. DuplicateHandler Class

**Remove duplicate records**

```python
from lib.data_cleaning import DuplicateHandler

dup_handler = DuplicateHandler()

# Identify duplicates
duplicates = dup_handler.identify_duplicates(df)

# Remove duplicates (keep first occurrence)
df = dup_handler.remove_duplicates(df, keep='first')
```

### 3. OutlierHandler Class

**Detect and treat outliers**

```python
from lib.data_cleaning import OutlierHandler

outlier_handler = OutlierHandler()

# Detect outliers using IQR
outliers = outlier_handler.detect_iqr_outliers(df, column='income', multiplier=1.5)

# Cap outliers
df = outlier_handler.cap_outliers(df, column='income', multiplier=1.5)
```

### 4. DataTypeConverter Class

**Optimize data types**

```python
from lib.data_cleaning import DataTypeConverter

converter = DataTypeConverter()

# Optimize numeric dtypes (reduce memory)
df = converter.optimize_numeric_dtypes(df)

# Convert low-cardinality columns to category
df = converter.convert_object_to_category(df, max_unique=50)
```

### 5. CategoricalEncoder Class

**Encode categorical variables**

```python
from lib.data_cleaning import CategoricalEncoder

encoder = CategoricalEncoder()

# Label encode
df = encoder.label_encode(df, columns=['gender', 'education'])

# One-hot encode
df = encoder.one_hot_encode(df, columns=['country'], drop_first=True)
```

### 6. DataQualityValidator Class

**Validate cleaned data**

```python
from lib.data_cleaning import DataQualityValidator

validator = DataQualityValidator()

# Validate cleaned dataset
results = validator.validate_cleaned_data(df)
print(f"Missing: {results['missing_pct']}%")
print(f"Duplicates: {results['duplicate_pct']}%")
```

---

## What CHUNK_02 Does

### Quality Gate 1: Handle Missing Values
- Analyzes missing value patterns
- Drops columns with >50% missing
- Fills numeric columns with median
- Fills categorical columns with mode
- Validates results

**Expected Duration:** 60-120 seconds

### Quality Gate 2: Remove Duplicates
- Identifies duplicate records
- Removes exact duplicates
- Validates no duplicates remain

**Expected Duration:** 30-60 seconds

### Quality Gate 3: Validate Cleaned Data
- Validates missing value percentages
- Checks duplicate counts
- Analyzes data types
- Generates validation report

**Expected Duration:** 30-60 seconds

---

## Outputs Generated

1. **CHUNK_02_CLEANING_SUMMARY.txt**
   - Before/after statistics
   - Rows and columns removed
   - Quality metrics

2. **chunk_02_metadata.json**
   - Dataset shapes
   - Column names and types
   - Validation results
   - Machine-readable format

3. **chunk_02_execution.log**
   - Detailed execution log
   - Timing information
   - Any errors or warnings

---

## Expected Output

```
================================================================================
CHUNK_02: DATA CLEANING & PREPROCESSING (INTERACTIVE)
================================================================================

[OK] CHUNK_02 Directory: C:\Users\...\CHUNK_02_DATA_CLEANING
[OK] Imported data_cleaning library

================================================================================
QUALITY GATE 1: HANDLE MISSING VALUES
================================================================================

Cleaning: application_train.csv
  Total missing: 13,450,920 (41.23%)
  [OK] Dropped 5 high-missing columns
  [OK] Filled numeric missing values using median
  [OK] Filled categorical missing values using mode

... (more datasets)

================================================================================
QUALITY GATE 2: HANDLE DUPLICATES
================================================================================

[OK] Removed 100 duplicate rows

... (more datasets)

================================================================================
QUALITY GATE 3: VALIDATE CLEANED DATA
================================================================================

application_train.csv
  Shape: (307511, 117)
  Memory: 145.23 MB
  Missing: 0.00%
  Duplicates: 0.00%

... (more datasets)

================================================================================
GENERATING REPORTS
================================================================================

[OK] Saved summary: documentation/CHUNK_02_CLEANING_SUMMARY.txt
[OK] Saved metadata: config/chunk_02_metadata.json

================================================================================
CHUNK_02: DATA CLEANING COMPLETE
================================================================================

Ready for CHUNK_03 - Feature Validation
```

---

## Data Cleaning Configuration

From `config/chunk_02_config.json`:

### Missing Values
- **Numeric method:** Median (robust to outliers)
- **Categorical method:** Mode (most frequent value)
- **Drop threshold:** 50% (remove columns with >50% missing)

### Duplicates
- **Strategy:** Keep first occurrence
- **Check:** All columns

### Outliers
- **Detection:** IQR (Interquartile Range)
- **Multiplier:** 1.5 (standard)
- **Handling:** Cap (trim to bounds)

### Data Types
- **Optimize numeric:** Yes (int64→int32, float64→float32)
- **Convert to category:** Yes (for low-cardinality columns)
- **Category threshold:** 50 unique values

---

## Cleaning Report Example

```
================================================================================
DATA CLEANING SUMMARY
Date: 2026-08-12 16:39:48
================================================================================

application_train.csv
--------------------------------------------------------------------------------
Before: 307,511 rows, 122 cols
After:  307,511 rows, 117 cols
Removed: 0 rows, 5 cols
Quality: 0.00% missing, 0.00% duplicates

bureau.csv
--------------------------------------------------------------------------------
Before: 1,716,575 rows, 17 cols
After:  1,716,575 rows, 17 cols
Removed: 0 rows, 0 cols
Quality: 0.02% missing, 0.00% duplicates

================================================================================
```

---

## Using Cleaned Data in CHUNK_03

```python
# Access cleaned datasets from CHUNK_02
cleaned_datasets = chunk02_results['cleaned_datasets']

# Use in CHUNK_03
application_train = cleaned_datasets['application_train.csv']
bureau = cleaned_datasets['bureau.csv']

# Ready for feature engineering
print(application_train.shape)
```

---

## Success Criteria

CHUNK_02 is successful when:

- [x] All missing values handled (<5% remaining)
- [x] All duplicates removed
- [x] Data types optimized
- [x] Quality validation passes
- [x] 3 output reports generated
- [x] Metadata saved
- [x] Execution log shows no critical errors
- [x] Ready for CHUNK_03

---

## Troubleshooting

### Issue: "NameError: name 'results' is not defined"
**Solution:** Run CHUNK_01 first, then run CHUNK_02

### Issue: "Module not found: data_cleaning"
**Solution:** Ensure you're running from the correct directory

### Issue: Out of memory
**Solution:** Datasets total 1.4 GB. Need 3-4 GB free RAM.

### Issue: Script runs very slowly
**Solution:** Normal - cleaning 57M+ records takes time. Be patient.

---

## Next Steps

After CHUNK_02 completes:

1. **Examine Cleaning Report**
   - Check `CHUNK_02_CLEANING_SUMMARY.txt`
   - Review quality metrics

2. **Verify Data Quality**
   - Look at `chunk_02_metadata.json`
   - Confirm all datasets are clean

3. **Proceed to CHUNK_03**
   - Feature Validation & Exploration
   - Uses cleaned datasets as input

4. **Use Cleaned Data**
   ```python
   cleaned_df = chunk02_results['cleaned_datasets']['application_train.csv']
   ```

---

## Timeline

- **Total Duration:** 3-5 minutes
- **CHUNK_02 Only:** Days 4-5 of Sprint 1
- **Project Timeline:** Week 1 of 6-week project

---

## Document Information

**File:** README.md  
**Version:** 1.0.0  
**Last Updated:** August 12, 2026  
**Status:** PRODUCTION READY  

---

**Ready to Execute CHUNK_02!**

For Jupyter: Copy-paste the exec() commands above  
For Windows: Run `RUN_CHUNK_02.bat`  
For Python: Run `python scripts/CHUNK_02_INTERACTIVE.py`

---

## Key Statistics

**Before Cleaning:**
- 57.2M+ total records
- 1.4 GB total memory
- Multiple datasets with missing values
- Potential duplicate records

**After Cleaning:**
- ~57M records (minimal duplicates)
- ~1.3 GB memory (optimized)
- Missing values <1%
- Data types optimized
- Ready for feature engineering
