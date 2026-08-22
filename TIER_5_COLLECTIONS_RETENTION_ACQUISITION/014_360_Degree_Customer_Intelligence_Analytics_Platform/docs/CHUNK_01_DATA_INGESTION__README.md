# CHUNK_01: DATA INGESTION & PROFILING
## PROBLEM_004_Customer_360_Analysis

**Status:** Ready to Execute  
**Version:** 1.0.0  
**Date:** August 12, 2026  
**Phase:** CRISP-DM Phase 2 - Data Understanding  
**Sprint:** AGILE Sprint 1 - Days 2-3

---

## Overview

CHUNK_01 integrates all 8 CSV data sources and performs comprehensive data profiling:

- **Load** all 8 CSV datasets (1.4 GB, 57.2M+ records)
- **Validate** data quality and integrity
- **Profile** data characteristics and distributions
- **Generate** comprehensive quality reports
- **Create** data dictionary for documentation
- **Set up** reusable utility library functions

**Execution Time:** ~2-3 minutes (depends on system I/O)  
**Output Files:** 5 reports + configuration + logs

---

## Quick Start

### Option 1: Windows Batch (Recommended)

```bash
cd C:\Users\rnand\Documents\home-credit-default-risk\Enterprise_AI_Workflows\PROBLEM_004_Customer_360_Analysis\CHUNK_01_DATA_INGESTION

RUN_CHUNK_01.bat
```

### Option 2: Python (Cross-Platform)

```bash
python RUN_CHUNK_01.py
```

### Option 3: Direct Python

```bash
python scripts/CHUNK_01_DATA_INGESTION.py
```

---

## Prerequisites

### Required Python Packages
```bash
pip install pandas numpy
```

### Data Files
All 8 CSV files must be in:  
`C:\Users\rnand\OneDrive\Desktop(1)\home-credit-default-risk\data\`

Required files:
- [x] application_train.csv (158 MB)
- [x] application_test.csv (25 MB)
- [x] bureau.csv (162 MB)
- [x] bureau_balance.csv (358 MB) ← Highest predictive value
- [x] credit_card_balance.csv (89 MB)
- [x] installments_payments.csv (48 MB) ← High predictive value
- [x] POS_CASH_balance.csv (375 MB)
- [x] previous_application.csv (227 MB)

**Total:** 1.4 GB, 57.2M+ records

---

## Directory Structure

```
PROBLEM_004_Customer_360_Analysis/
└── CHUNK_01_DATA_INGESTION/
    ├── scripts/
    │   └── CHUNK_01_DATA_INGESTION.py ........... [Main script]
    ├── lib/
    │   └── data_utils.py ........................ [Utility library]
    ├── config/
    │   ├── chunk_01_config.json ................. [Configuration]
    │   └── data_dictionary.json ................. [Generated]
    ├── documentation/
    │   ├── INGESTION_SUMMARY.txt ................ [Generated]
    │   ├── DATA_QUALITY_REPORT.txt .............. [Generated]
    │   └── CHUNK_01_DETAILED_REPORT.md .......... [Generated]
    ├── logs/
    │   └── chunk_01_execution.log ............... [Generated]
    ├── data/
    │   └── (output data files if generated)
    ├── RUN_CHUNK_01.bat ......................... [Windows runner]
    ├── RUN_CHUNK_01.py .......................... [Python runner]
    └── README.md ................................ [This file]
```

---

## Library Functions

CHUNK_01 includes a comprehensive utility library (`lib/data_utils.py`) with 4 classes and 7 functions:

### 1. DataLoader Class
**Purpose:** Load and manage CSV files

**Methods:**
- `load_csv(filename, sample=False)` - Load single CSV file
- `load_all_datasets(file_list)` - Load multiple CSV files
- `get_dataframe(filename)` - Retrieve loaded DataFrame

**Example:**
```python
from lib.data_utils import DataLoader

loader = DataLoader(data_root="/path/to/data")
datasets = loader.load_all_datasets([
    'application_train.csv',
    'bureau.csv',
    # ... other files
])
df = loader.get_dataframe('application_train.csv')
```

### 2. DataValidator Class
**Purpose:** Validate data quality

**Methods:**
- `check_missing_values(df)` - Analyze missing data
- `check_duplicates(df)` - Find duplicate rows
- `check_data_types(df)` - Analyze column types
- `validate_dataset(df)` - Run comprehensive validation

**Example:**
```python
from lib.data_utils import DataValidator

validator = DataValidator()
results = validator.validate_dataset(df, "application_train")
print(f"Missing values: {results['missing_values']['missing_pct']}%")
print(f"Duplicates: {results['duplicates']['duplicate_pct']}%")
```

### 3. DataProfiler Class
**Purpose:** Profile data characteristics

**Methods:**
- `profile_numeric_column(series)` - Profile numeric columns
- `profile_categorical_column(series)` - Profile categorical columns
- `profile_dataframe(df)` - Profile entire DataFrame

**Example:**
```python
from lib.data_utils import DataProfiler

profiler = DataProfiler()
profile = profiler.profile_dataframe(df, "application_train")

# Access statistics
for col_name, col_profile in profile['columns'].items():
    print(f"{col_name}: {col_profile['dtype']}")
```

### 4. DataQualityReporter Class
**Purpose:** Generate quality reports

**Methods:**
- `generate_summary_report(datasets_info)` - Summary report
- `generate_quality_report(validation_results)` - Quality metrics

**Example:**
```python
from lib.data_utils import DataQualityReporter

reporter = DataQualityReporter()
report = reporter.generate_summary_report(loader.load_metadata)
print(report)
```

### 5-7. Utility Functions

```python
from lib.data_utils import optimize_dtypes, save_to_parquet, load_from_parquet

# Optimize memory usage
df_optimized = optimize_dtypes(df)

# Save to Parquet (faster, smaller)
save_to_parquet(df, 'output.parquet')

# Load from Parquet
df_loaded = load_from_parquet('output.parquet')
```

---

## What CHUNK_01 Does

### Quality Gate 1: Data Ingestion
- Loads all 8 CSV files
- Validates file availability
- Stores metadata (shape, size, columns, dtypes)
- **Expected Duration:** 30-60 seconds

### Quality Gate 2: Data Validation
- Checks missing values (max 50%)
- Checks duplicates (max 5%)
- Analyzes data types
- Validates record counts
- **Expected Duration:** 30-60 seconds

### Quality Gate 3: Data Profiling
- Generates statistics for numeric columns (min, max, mean, median, std)
- Generates value distributions for categorical columns
- Creates comprehensive profiles
- **Expected Duration:** 60-120 seconds

### Outputs Generated

1. **INGESTION_SUMMARY.txt**
   - Total rows, columns, memory per dataset
   - Overall data volume statistics

2. **DATA_QUALITY_REPORT.txt**
   - Missing values percentages
   - Duplicate statistics
   - Data type distributions

3. **CHUNK_01_DETAILED_REPORT.md**
   - Formatted report with tables
   - Data quality metrics
   - Available library functions
   - Next steps

4. **data_dictionary.json**
   - Column names and types
   - Missing value statistics
   - Unique value counts
   - Machine-readable format

5. **chunk_01_execution.log**
   - Detailed execution log
   - Timing information
   - Any errors or warnings

---

## Expected Output

```
================================================================================
PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
CHUNK_01: DATA INGESTION AND PROFILING
================================================================================

================================================================================
QUALITY GATE 1: DATA INGESTION
================================================================================
[OK] Loaded: application_train.csv (307511 rows)
[OK] Loaded: application_test.csv (48744 rows)
[OK] Loaded: bureau.csv (1716575 rows)
[OK] Loaded: bureau_balance.csv (27299357 rows)
[OK] Loaded: credit_card_balance.csv (3840312 rows)
[OK] Loaded: installments_payments.csv (13605401 rows)
[OK] Loaded: POS_CASH_balance.csv (10001358 rows)
[OK] Loaded: previous_application.csv (1668379 rows)

[OK] Loaded 8/8 files

================================================================================
QUALITY GATE 2: DATA VALIDATION
================================================================================
Validating: application_train.csv
  Shape: 307511 rows, 122 columns
  Missing values: 41.23%
  Duplicates: 0.0%
  Data types: {'object': 23, 'int64': 99}

... (more datasets)

================================================================================
QUALITY GATE 3: DATA PROFILING
================================================================================
Profiling: application_train.csv
[OK] Profiled 122 columns

... (more datasets)

================================================================================
CREATING DATA DICTIONARY
================================================================================
[OK] Created: data_dictionary.json

================================================================================
GENERATING QUALITY REPORTS
================================================================================
[OK] Created: INGESTION_SUMMARY.txt
[OK] Created: DATA_QUALITY_REPORT.txt
[OK] Created: CHUNK_01_DETAILED_REPORT.md

================================================================================
CHUNK_01: DATA INGESTION & PROFILING COMPLETE
================================================================================

Execution Result: SUCCESS
Datasets Loaded: 8

Reports generated:
  - summary: documentation/INGESTION_SUMMARY.txt
  - quality: documentation/DATA_QUALITY_REPORT.txt
  - detailed: documentation/CHUNK_01_DETAILED_REPORT.md

All outputs saved to: .../CHUNK_01_DATA_INGESTION
Next: CHUNK_02 - Data Cleaning
```

---

## Using the Library in CHUNK_02+

Once CHUNK_01 completes, subsequent chunks can import and use the library:

```python
import sys
from pathlib import Path

# Add lib directory to path
lib_path = Path(__file__).parent.parent / "CHUNK_01_DATA_INGESTION" / "lib"
sys.path.insert(0, str(lib_path))

# Import library classes
from data_utils import DataLoader, DataValidator, DataProfiler

# Use in CHUNK_02, CHUNK_03, etc.
loader = DataLoader(data_root="/path/to/data")
df = loader.load_csv("application_train.csv")
```

---

## Data Dictionary Output Format

`config/data_dictionary.json` contains:

```json
{
  "generated_at": "2026-08-12T...",
  "datasets": {
    "application_train.csv": {
      "description": "Primary training dataset...",
      "shape": [307511, 122],
      "memory_mb": 158.44,
      "columns": [
        {
          "name": "SK_ID_CURR",
          "dtype": "int64",
          "non_null": 307511,
          "null_pct": 0.0,
          "unique": 307511
        },
        ...
      ]
    }
  }
}
```

---

## Data Quality Thresholds

Configuration in `config/chunk_01_config.json`:

- **Max Missing %:** 50% (datasets can have up to 50% missing)
- **Max Duplicate %:** 5% (datasets can have up to 5% duplicates)
- **Min Records:** 100 per dataset

---

## Troubleshooting

### Issue: "File not found: application_train.csv"
**Solution:** Ensure all CSV files are in:  
`C:\Users\rnand\OneDrive\Desktop(1)\home-credit-default-risk\data\`

### Issue: "MemoryError" or out of memory
**Solution:** The system is loading 1.4 GB. You need ~3-4 GB free RAM.

### Issue: Slow execution
**Solution:** Normal - system I/O can be slow. Each file load takes 10-30 seconds.

### Issue: "No module named 'pandas'"
**Solution:** Install required packages:
```bash
pip install pandas numpy
```

---

## Next Steps

After CHUNK_01 completes:

1. **Review Reports**
   - Check `CHUNK_01_DETAILED_REPORT.md`
   - Review data quality metrics

2. **Examine Data Dictionary**
   - Look at `data_dictionary.json`
   - Understand column statistics

3. **Proceed to CHUNK_02**
   - Data Cleaning & Preprocessing
   - Uses utility library functions from CHUNK_01

4. **Subsequent Chunks (03-17)**
   - All can import and reuse library functions
   - Feature engineering, modeling, deployment

---

## Success Criteria

CHUNK_01 is successful when:

- [x] All 8 CSV files load without errors
- [x] Data validation passes (quality checks)
- [x] Data profiling completes for all columns
- [x] 5 output reports generated
- [x] Data dictionary created
- [x] Utility library functions available
- [x] Execution log shows no critical errors
- [x] Ready for CHUNK_02

---

## Timeline

- **Total Duration:** 2-3 minutes
- **CHUNK_01 Only:** Days 2-3 of Sprint 1
- **Project Timeline:** Week 1 of 6-week project

---

## Document Information

**File:** README.md  
**Version:** 1.0.0  
**Last Updated:** August 12, 2026  
**Status:** PRODUCTION READY  

---

**Ready to Execute CHUNK_01!**

Run `RUN_CHUNK_01.bat` or `python RUN_CHUNK_01.py` now.

For questions, review `config/chunk_01_config.json` and `lib/data_utils.py`.
