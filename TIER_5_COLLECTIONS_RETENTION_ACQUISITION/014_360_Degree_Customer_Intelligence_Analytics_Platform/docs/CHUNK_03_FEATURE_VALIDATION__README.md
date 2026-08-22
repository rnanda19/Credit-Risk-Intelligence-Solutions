# CHUNK_03: FEATURE VALIDATION & EXPLORATION
## PROBLEM_004_Customer_360_Analysis

**Status:** Ready to Execute  
**Version:** 1.0.0  
**Date:** August 12, 2026  
**Phase:** CRISP-DM Phase 2 - Data Understanding  
**Sprint:** AGILE Sprint 1 - Days 5-6

---

## Overview

CHUNK_03 validates and explores all features in cleaned datasets from CHUNK_02:

- **Analyze** feature distributions (numeric & categorical)
- **Compute** correlation matrices and identify high correlations
- **Assess** feature quality scores
- **Validate** statistical properties (normality, skewness, outliers)
- **Generate** comprehensive exploration reports
- **Identify** feature engineering opportunities

**Execution Time:** ~2-3 minutes  
**Output Files:** 3 reports + metadata + analyses

---

## Quick Start

### Option 1: Jupyter Notebook (Recommended)

```python
# Run CHUNK_01 and CHUNK_02 first to get cleaned datasets
exec(open(r'C:\Users\rnand\...\CHUNK_01_DATA_INGESTION\scripts\CHUNK_01_INTERACTIVE.py').read())
exec(open(r'C:\Users\rnand\...\CHUNK_02_DATA_CLEANING\scripts\CHUNK_02_INTERACTIVE.py').read())

# Then run CHUNK_03
exec(open(r'C:\Users\rnand\...\CHUNK_03_FEATURE_VALIDATION\scripts\CHUNK_03_INTERACTIVE.py').read())

# Use results
chunk03_results = run_chunk03(cleaned_datasets=chunk02_results['cleaned_datasets'])
```

### Option 2: Windows Batch

```bash
cd C:\Users\rnand\...\CHUNK_03_FEATURE_VALIDATION
RUN_CHUNK_03.bat
```

### Option 3: Python Script

```bash
python scripts/CHUNK_03_INTERACTIVE.py
```

**Execution Time:** 2-3 minutes

---

## Prerequisites

### Required Python Packages
```bash
pip install pandas numpy scipy
```

### Input Data
Requires cleaned datasets from CHUNK_02:
- All 8 cleaned datasets

---

## Library Functions

### 1. FeatureDistributionAnalyzer Class

**Analyze feature distributions**

```python
from lib.feature_validation import FeatureDistributionAnalyzer

analyzer = FeatureDistributionAnalyzer()

# Analyze single numeric feature
numeric_analysis = analyzer.analyze_numeric_distribution(df['income'], 'income')
# Returns: min, max, mean, median, std, skewness, kurtosis, etc.

# Analyze single categorical feature
categorical_analysis = analyzer.analyze_categorical_distribution(df['country'], 'country')
# Returns: unique values, top categories, percentages, etc.

# Analyze all features
all_features = analyzer.analyze_all_features(df)
# Returns: dictionary with analysis for each feature
```

### 2. CorrelationAnalyzer Class

**Analyze feature correlations**

```python
from lib.feature_validation import CorrelationAnalyzer

corr_analyzer = CorrelationAnalyzer()

# Compute correlation matrix
corr_matrix = corr_analyzer.compute_correlation_matrix(df, method='pearson')

# Find highly correlated pairs (>0.8)
high_corr_pairs = corr_analyzer.find_high_correlations(corr_matrix, threshold=0.8)
# Returns: [(feature1, feature2, correlation), ...]

# Full correlation analysis
correlation_analysis = corr_analyzer.analyze_feature_correlations(df, target='target')
```

### 3. FeatureQualityAssessor Class

**Assess feature quality**

```python
from lib.feature_validation import FeatureQualityAssessor

quality_assessor = FeatureQualityAssessor()

# Assess quality for all features
quality_scores = quality_assessor.assess_feature_quality(df)
# Returns: quality score (0-100) for each feature

# Identify low-quality features
low_quality = quality_assessor.identify_low_quality_features(df, threshold=50.0)
# Returns: list of features with quality < threshold
```

### 4. StatisticalValidator Class

**Validate features statistically**

```python
from lib.feature_validation import StatisticalValidator

validator = StatisticalValidator()

# Test normality (Shapiro-Wilk test)
normality_results = validator.test_normality(df['income'])
# Returns: test statistic, p-value, normal (yes/no)

# Detect skewness
skewness_analysis = validator.detect_skewness(df['income'])
# Returns: skewness value, type (symmetric/right/left), magnitude

# Detect outliers using z-score or IQR
outliers = validator.detect_outliers_statistical(df['income'], method='zscore')
# Returns: outlier count, percentage, detection method
```

### 5. ExplorationReportGenerator Class

**Generate exploration reports**

```python
from lib.feature_validation import ExplorationReportGenerator

reporter = ExplorationReportGenerator()

# Generate feature report
feature_report = reporter.generate_feature_report(df, features_analysis)
# Returns: formatted text report
```

---

## What CHUNK_03 Does

### Quality Gate 1: Feature Distribution Analysis
- Analyzes all numeric features (mean, std, skewness, kurtosis)
- Analyzes all categorical features (unique values, top categories)
- Identifies data types and completeness
- Validates feature ranges

**Expected Duration:** 30-60 seconds

### Quality Gate 2: Correlation Analysis
- Computes Pearson correlation matrix
- Identifies feature pairs with correlation >0.8
- Detects multicollinearity issues
- Analyzes target correlations (if applicable)

**Expected Duration:** 30-60 seconds

### Quality Gate 3: Feature Quality Assessment
- Computes quality scores (0-100) for each feature
- Evaluates completeness and variety
- Identifies low-quality features
- Flags features for potential removal

**Expected Duration:** 30-60 seconds

### Quality Gate 4: Statistical Validation
- Tests feature normality
- Detects skewness and kurtosis
- Identifies outliers using statistical methods
- Validates statistical properties

**Expected Duration:** 30-60 seconds

---

## Outputs Generated

1. **CHUNK_03_EXPLORATION_SUMMARY.txt**
   - Feature statistics by dataset
   - Distribution summaries
   - Correlation findings

2. **chunk_03_metadata.json**
   - Features analyzed count
   - High correlation pairs
   - Quality scores
   - Machine-readable format

3. **chunk_03_execution.log**
   - Detailed execution log
   - Timing information
   - Validation results

---

## Expected Output

```
================================================================================
CHUNK_03: FEATURE VALIDATION & EXPLORATION (INTERACTIVE)
================================================================================

[OK] CHUNK_03 Directory: C:\Users\...\CHUNK_03_FEATURE_VALIDATION
[OK] Imported feature_validation library

================================================================================
QUALITY GATE 1: FEATURE DISTRIBUTION ANALYSIS
================================================================================

Analyzing: application_train.csv
  [OK] Analyzed 122 features
  Numeric features: 99
  Categorical features: 23

... (more datasets)

================================================================================
QUALITY GATE 2: CORRELATION ANALYSIS
================================================================================

Analyzing correlations: application_train.csv
  [OK] Computed pearson correlation for 99 features
  [OK] Found 45 highly correlated pairs (>0.8)

... (more datasets)

================================================================================
QUALITY GATE 3: FEATURE QUALITY ASSESSMENT
================================================================================

Assessing quality: application_train.csv
  Average quality score: 87.34/100
  Low-quality features: 8

... (more datasets)

================================================================================
QUALITY GATE 4: STATISTICAL VALIDATION
================================================================================

Validating: application_train.csv
  Total features: 122
  Numeric features: 99
  Categorical features: 23

================================================================================
GENERATING EXPLORATION REPORTS
================================================================================

[OK] Saved summary: documentation/CHUNK_03_EXPLORATION_SUMMARY.txt
[OK] Saved metadata: config/chunk_03_metadata.json

================================================================================
CHUNK_03: FEATURE VALIDATION & EXPLORATION COMPLETE
================================================================================

Ready for CHUNK_04 - Feature Engineering
```

---

## Feature Quality Scoring

Quality Score = (Completeness × 0.7) + (Variety × 0.3)

- **Completeness:** Percentage of non-missing values (0-100)
- **Variety:** Percentage of unique values (0-100, capped at 100)
- **Score Range:** 0-100 (100 = perfect quality)

### Quality Tiers
- **High Quality:** 80-100
- **Medium Quality:** 50-80
- **Low Quality:** <50 (candidates for removal or engineering)

---

## Correlation Interpretation

### High Correlation (>0.8)
- Features carry redundant information
- May cause multicollinearity issues
- Consider removing one feature
- Useful for feature engineering (ratio, difference)

### Medium Correlation (0.5-0.8)
- Features have moderate linear relationship
- May be useful together
- Monitor in modeling

### Low Correlation (<0.5)
- Features are largely independent
- Useful for model diversity
- Good candidates for feature selection

---

## Using Validation Results in CHUNK_04

```python
# Access validation results from CHUNK_03
features_analysis = chunk03_results['features_analysis']
correlations = chunk03_results['correlation_results']
quality = chunk03_results['quality_results']

# Use for feature engineering
for dataset_name, quality_scores in quality.items():
    low_quality_features = [f for f, s in quality_scores.items()
                           if s.get('quality_score', 0) < 50]
    print(f"Remove from {dataset_name}: {low_quality_features}")

# Use for feature selection
for dataset_name, corr in correlations.items():
    high_corr_pairs = corr['high_correlations']
    print(f"Redundant features in {dataset_name}: {high_corr_pairs}")
```

---

## Success Criteria

CHUNK_03 is successful when:

- [x] All features analyzed for distribution
- [x] Correlations computed and high-correlation pairs identified
- [x] Feature quality scores generated
- [x] Statistical properties validated
- [x] 3 output reports generated
- [x] Metadata saved
- [x] Execution log shows no critical errors
- [x] Insights guide feature engineering (CHUNK_04)

---

## Statistical Tests Used

### Normality Testing
- **Shapiro-Wilk Test** - Tests if data is normally distributed
- P-value > 0.05 indicates normality

### Skewness Analysis
- **Positive Skew:** Right tail (mean > median)
- **Negative Skew:** Left tail (mean < median)
- **Magnitude:** Low (<0.5), Moderate (0.5-1), High (>1)

### Outlier Detection
- **Z-Score Method:** |z| > 3 indicates outlier
- **IQR Method:** Beyond Q1-1.5×IQR or Q3+1.5×IQR

---

## Troubleshooting

### Issue: "NameError: name 'chunk02_results' is not defined"
**Solution:** Run CHUNK_02 first to get cleaned datasets

### Issue: "Module not found: feature_validation"
**Solution:** Ensure you're running from correct directory

### Issue: Script runs slowly
**Solution:** Large datasets take time. Correlation computation is O(n²). Be patient.

### Issue: Low correlation findings despite high-dimension data
**Solution:** Normal - many real-world features are weakly correlated

---

## Next Steps

After CHUNK_03 completes:

1. **Review Exploration Report**
   - Check `CHUNK_03_EXPLORATION_SUMMARY.txt`
   - Understand feature distributions

2. **Analyze Correlations**
   - Look at high-correlation pairs
   - Plan feature interactions
   - Identify redundant features

3. **Assess Quality**
   - Review quality scores
   - Plan feature engineering for low-quality features
   - Decide on feature removal

4. **Proceed to CHUNK_04**
   - Feature Engineering
   - Create new features
   - Select best features

---

## Timeline

- **Total Duration:** 2-3 minutes
- **CHUNK_03 Only:** Days 5-6 of Sprint 1
- **Project Timeline:** Week 1 of 6-week project

---

## Key Statistics

**Before Exploration (CHUNK_02 output):**
- ~57M records
- ~245 columns
- ~1.3 GB memory
- <1% missing values

**After Exploration (CHUNK_03 output):**
- Same data
- Complete feature analysis
- Correlation map
- Quality scores
- Feature engineering recommendations

---

## Document Information

**File:** README.md  
**Version:** 1.0.0  
**Last Updated:** August 12, 2026  
**Status:** PRODUCTION READY  

---

**Ready to Execute CHUNK_03!**

For Jupyter: Copy-paste the exec() commands above  
For Windows: Run `RUN_CHUNK_03.bat`  
For Python: Run `python scripts/CHUNK_03_INTERACTIVE.py`
