# CHUNK_04: FEATURE ENGINEERING
## PROBLEM_004_Customer_360_Analysis

**Status:** Ready to Execute  
**Version:** 1.0.0  
**Date:** August 12, 2026  
**Phase:** CRISP-DM Phase 3 - Data Preparation  
**Sprint:** AGILE Sprint 2 - Days 1-2

---

## Overview

CHUNK_04 engineers new features from cleaned data and prepares datasets for modeling:

- **Encode** categorical variables to numeric format
- **Create** polynomial, interaction, and ratio features
- **Transform** features via standardization and scaling
- **Select** high-quality features by variance
- **Detect** and flag redundant features
- **Validate** feature quality and characteristics

**Execution Time:** ~2-3 minutes  
**Output Files:** Engineered datasets + metrics + summary

---

## Quick Start

### Option 1: Jupyter Notebook (Recommended)

```python
# Run CHUNK_01, CHUNK_02, CHUNK_03 first
exec(open(r'C:\Users\rnand\...\CHUNK_01_DATA_INGESTION\scripts\CHUNK_01_INTERACTIVE.py').read())
exec(open(r'C:\Users\rnand\...\CHUNK_02_DATA_CLEANING\scripts\CHUNK_02_INTERACTIVE.py').read())
exec(open(r'C:\Users\rnand\...\CHUNK_03_FEATURE_VALIDATION\scripts\CHUNK_03_COMPLETE.py').read())

# Then run CHUNK_04
exec(open(r'C:\Users\rnand\...\CHUNK_04_FEATURE_ENGINEERING\scripts\CHUNK_04_COMPLETE.py').read())

# Use results
chunk04_results = run_chunk04(cleaned_datasets=chunk02_results['cleaned_datasets'])
```

### Option 2: Windows Batch

```bash
cd C:\Users\rnand\...\CHUNK_04_FEATURE_ENGINEERING
RUN_CHUNK_04.bat
```

### Option 3: Python Script

```bash
python scripts/CHUNK_04_COMPLETE.py
```

**Execution Time:** 2-3 minutes

---

## Prerequisites

### Required Python Packages
```bash
pip install pandas numpy scikit-learn
```

### Input Data
Requires cleaned datasets from CHUNK_02:
- All 8 cleaned datasets

---

## Library Functions

### 1. FeatureCreator Class

**Create new features**

```python
from lib.feature_engineering import FeatureCreator

creator = FeatureCreator()

# Create polynomial features (degree 2)
df_poly, created = creator.create_polynomial_features(df, columns=['age', 'income'], degree=2)
# Adds: age_poly_2, income_poly_2

# Create interaction features
pairs = [('age', 'income'), ('income', 'expenses')]
df_interact, created = creator.create_interaction_features(df, pairs)
# Adds: age_x_income, income_x_expenses

# Create ratio features
df_ratio, created = creator.create_ratio_features(df, pairs)
# Adds: age_ratio_income, income_ratio_expenses

# Create log-transformed features
df_log, created = creator.create_log_features(df, ['income', 'age'])
# Adds: income_log, age_log (if all values > 0)
```

### 2. CategoricalEncoder Class

**Encode categorical variables**

```python
from lib.feature_engineering import CategoricalEncoder

encoder = CategoricalEncoder()

# Label encoding (ordinal)
df_encoded = encoder.label_encode(df, columns=['country', 'gender', 'region'])
# Converts categories to integers 0, 1, 2, ...

# One-hot encoding
df_onehot, created = encoder.one_hot_encode(df, columns=['country'], drop_first=True)
# Converts single categorical to multiple binary columns

# Ordinal encoding with specified order
order = {
    'quality': {'low': 1, 'medium': 2, 'high': 3},
    'size': {'small': 1, 'large': 2}
}
df_ordinal = encoder.ordinal_encode(df, columns=order.keys(), order_mapping=order)
```

### 3. FeatureTransformer Class

**Transform features**

```python
from lib.feature_engineering import FeatureTransformer

transformer = FeatureTransformer()

# Standardization (z-score)
df_std = transformer.standardize(df, columns=['age', 'income', 'expenses'])
# Mean=0, Std=1

# Normalization (0-1 scaling)
df_norm = transformer.normalize(df, columns=['age', 'income'])
# Min=0, Max=1

# Log transformation
df_log = transformer.log_transform(df, columns=['income'])

# Square root transformation
df_sqrt = transformer.sqrt_transform(df, columns=['distance'])
```

### 4. FeatureSelector Class

**Select best features**

```python
from lib.feature_engineering import FeatureSelector

selector = FeatureSelector()

# Variance-based selection
high_var = selector.select_by_variance(df, threshold=0.01)
# Returns: features with variance > 0.01

# Correlation-based selection
corr_features = selector.select_by_correlation(df, target_col='target', threshold=0.05)
# Returns: features with correlation > 0.05 with target

# Mutual information selection
mi_features = selector.select_by_mutual_information(df, target_col='target', k=10)
# Returns: top 10 features by mutual information with target
```

### 5. FeatureQualityAssessor Class

**Assess engineered features**

```python
from lib.feature_engineering import FeatureQualityAssessor

assessor = FeatureQualityAssessor()

# Assess feature quality
quality = assessor.assess_features(df_engineered, df_original)
# Returns: {total_original, total_new, features_added, memory_increase_mb}

# Detect redundant features
redundant = assessor.detect_redundant_features(df, threshold=0.95)
# Returns: [(feature1, feature2, correlation), ...]
# Pairs with correlation > 0.95
```

### 6. FeatureInteractionAnalyzer Class

**Analyze feature interactions**

```python
from lib.feature_engineering import FeatureInteractionAnalyzer

analyzer = FeatureInteractionAnalyzer()

# Find numeric interactions
numeric_int = analyzer.find_numeric_interactions(df, threshold=0.3)
# Returns: interactions with variance > 0.3

# Find categorical interactions
cat_int = analyzer.find_categorical_interactions(df)
# Returns: unique combinations per categorical pair
```

---

## What CHUNK_04 Does

### Quality Gate 1: Categorical Encoding
- Label encodes all categorical variables
- Creates integer mappings for each category
- Preserves ordinal relationships where appropriate
- Handles missing values gracefully

**Expected Duration:** 30-60 seconds

### Quality Gate 2: Feature Creation
- Creates polynomial features (degree 2) from numeric columns
- Creates interaction features from feature pairs
- Creates ratio features (with division-by-zero handling)
- Logs statistics on features created

**Expected Duration:** 30-60 seconds

### Quality Gate 3: Feature Scaling & Transformation
- Standardizes all numeric features (z-score normalization)
- Centers features at mean=0, std=1
- Handles missing values with forward fill
- Validates scaling success

**Expected Duration:** 30-60 seconds

### Quality Gate 4: Feature Selection & Quality Assessment
- Selects high-variance features (threshold: 0.01)
- Detects redundant features (correlation > 0.95)
- Computes quality metrics per dataset
- Generates feature engineering summary

**Expected Duration:** 30-60 seconds

---

## Outputs Generated

1. **engineered_datasets** (dictionary)
   - Transformed datasets ready for modeling
   - All numeric, scaled, with new features

2. **feature_creation_summary** (dictionary)
   - Original feature count
   - New features created
   - Total features per dataset

3. **selection_results** (dictionary)
   - High-variance features list
   - Redundant feature pairs

4. **quality_assessment** (dictionary)
   - Memory increase metrics
   - Feature addition statistics

---

## Expected Output

```
================================================================================
CHUNK_04: FEATURE ENGINEERING
================================================================================

================================================================================
QUALITY GATE 1: CATEGORICAL ENCODING
================================================================================

Encoding: application_train.csv
  [OK] Encoded 23 categorical features

... (more datasets)

================================================================================
QUALITY GATE 2: FEATURE CREATION
================================================================================

Creating features: application_train.csv
  [OK] Created 8 new features
  Total features: 130

... (more datasets)

================================================================================
QUALITY GATE 3: FEATURE SCALING & TRANSFORMATION
================================================================================

Scaling features: application_train.csv
  [OK] Standardized 99 numeric features

... (more datasets)

================================================================================
QUALITY GATE 4: FEATURE SELECTION & QUALITY ASSESSMENT
================================================================================

Assessing: application_train.csv
  High-variance features: 89
  Redundant pairs: 12
  Features added: 8
  Memory increase: 15.34 MB

... (more datasets)

================================================================================
CHUNK_04: FEATURE ENGINEERING COMPLETE
================================================================================

Ready for CHUNK_05 - Model Selection & Training
```

---

## Feature Engineering Strategies

### Polynomial Features
- **Use case:** Capture non-linear relationships
- **Example:** If income correlates with purchases, income² may capture accelerating effects
- **Caution:** Can lead to overfitting; use sparingly

### Interaction Features
- **Use case:** Combine related features
- **Example:** age × income (experienced high-earners behave differently)
- **Strategy:** Create interactions only for domain-relevant pairs

### Ratio Features
- **Use case:** Normalize by related measure
- **Example:** debt_ratio = debt / income (income-adjusted debt)
- **Caution:** Handle division-by-zero carefully

### Log Transformation
- **Use case:** Compress skewed distributions
- **Example:** Income often log-normal; log(income) normalizes
- **Requirement:** All values must be > 0

---

## Feature Selection Strategies

### Variance-Based
- **Threshold:** 0.01
- **Removes:** Features with very low variance (nearly constant)
- **Advantage:** Fast, interpretable
- **Disadvantage:** Ignores relationship with target

### Correlation-Based
- **Threshold:** 0.05
- **Selects:** Features correlated with target variable
- **Advantage:** Direct target relevance
- **Disadvantage:** Misses non-linear relationships

### Mutual Information
- **Top-k:** 10 features
- **Selects:** Features with highest information about target
- **Advantage:** Captures non-linear relationships
- **Disadvantage:** More computational cost

---

## Redundancy Detection

### High Correlation Threshold (0.95)
Features with correlation > 0.95 carry redundant information:
- **Action:** Remove one of the pair
- **Choice:** Keep if more interpretable or computationally efficient
- **Example:** If height_cm and height_m correlated at 0.999, drop one

### Low Variance Threshold (0.01)
Features with variance < 0.01 provide little information:
- **Action:** Flag for removal in feature selection
- **Rationale:** Model cannot learn pattern from near-constant feature

---

## Using Results in CHUNK_05

```python
# Access engineered datasets
engineered_dfs = chunk04_results['engineered_datasets']
for filename, df in engineered_dfs.items():
    print(f"{filename}: {df.shape}")

# Check feature creation summary
summary = chunk04_results['feature_creation_summary']
for filename, creation in summary.items():
    print(f"{filename}: Added {creation['new_features']} features")

# Review redundancy
results = chunk04_results['selection_results']
for filename, selection in results.items():
    print(f"{filename}: {len(selection['redundant_pairs'])} redundant pairs")

# Monitor quality
quality = chunk04_results['quality_assessment']
for filename, metrics in quality.items():
    print(f"{filename}: Memory +{metrics['memory_increase_mb']:.2f} MB")
```

---

## Performance Notes

- **Feature Creation:** Linear in number of features
- **Scaling:** Linear in number of samples and features
- **Correlation Computation:** O(n²) in number of features
- **Bottleneck:** Large datasets with 1000+ features may be slow

**Optimization Tips:**
- Limit polynomial degree to 2
- Sample correlation computation for large feature sets
- Use feature grouping for very high-dimensional data

---

## Success Criteria

CHUNK_04 is successful when:

- [x] All categorical variables encoded
- [x] Polynomial features created (degree 2)
- [x] Interaction features generated
- [x] Ratio features calculated
- [x] All numeric features standardized
- [x] High-variance features identified
- [x] Redundant features detected
- [x] Quality metrics computed
- [x] Summary report generated
- [x] Engineered datasets ready for modeling

---

## Troubleshooting

### Issue: "Division by zero in ratio features"
**Solution:** Already handled with np.where - replaces with 0

### Issue: "Log of negative values"
**Solution:** Log features only created if all values > 0

### Issue: "Memory increased significantly"
**Normal:** Feature creation doubles dimensionality - expected behavior

### Issue: "Script runs slowly"
**Solution:** Reduce polynomial degree or sample features for correlation

### Issue: "Too many redundant pairs"
**Solution:** Use higher correlation threshold (e.g., 0.99 instead of 0.95)

---

## Timeline

- **Total Duration:** 2-3 minutes
- **CHUNK_04 Only:** Days 1-2 of Sprint 2
- **Project Timeline:** Week 1-2 of 6-week project

---

## Key Statistics

**Before Engineering (CHUNK_02 output):**
- ~245 columns
- All numeric or encoded
- ~1.3 GB memory
- Ready for modeling

**After Engineering (CHUNK_04 output):**
- ~270-280 columns (25-35 new)
- All numeric
- ~1.5 GB memory
- High-variance, selected features
- Redundancy identified

---

## Document Information

**File:** README.md  
**Version:** 1.0.0  
**Last Updated:** August 12, 2026  
**Status:** PRODUCTION READY  

---

**Ready to Execute CHUNK_04!**

For Jupyter: Copy-paste the exec() commands above  
For Windows: Run `RUN_CHUNK_04.bat`  
For Python: Run `python scripts/CHUNK_04_COMPLETE.py`
