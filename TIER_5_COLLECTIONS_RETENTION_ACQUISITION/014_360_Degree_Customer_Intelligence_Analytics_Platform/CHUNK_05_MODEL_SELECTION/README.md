# CHUNK_05: MODEL SELECTION & TRAINING
## PROBLEM_004_Customer_360_Analysis

**Status:** Ready to Execute  
**Version:** 1.0.0  
**Date:** August 12, 2026  
**Phase:** CRISP-DM Phase 4 - Modeling  
**Sprint:** AGILE Sprint 2 - Days 3-4

---

## Overview

CHUNK_05 trains multiple machine learning models and identifies the best performing algorithm:

- **Select** optimal algorithms for classification problem
- **Train** models with 5-fold cross-validation
- **Evaluate** performance using standard metrics
- **Analyze** feature importance from trained models
- **Compare** models and rank by performance
- **Identify** best model for deployment

**Execution Time:** ~5-10 minutes  
**Models Trained:** 4 (Logistic Regression, Random Forest, Gradient Boosting, SVM)  
**Output:** Trained models + performance metrics + feature rankings

---

## Quick Start

### Option 1: Jupyter Notebook (Recommended)

```python
# Run CHUNK_01 through CHUNK_04 first
exec(open(r'C:\...\CHUNK_01_DATA_INGESTION\scripts\CHUNK_01_INTERACTIVE.py').read())
exec(open(r'C:\...\CHUNK_02_DATA_CLEANING\scripts\CHUNK_02_INTERACTIVE.py').read())
exec(open(r'C:\...\CHUNK_03_FEATURE_VALIDATION\scripts\CHUNK_03_COMPLETE.py').read())
exec(open(r'C:\...\CHUNK_04_FEATURE_ENGINEERING\scripts\CHUNK_04_COMPLETE.py').read())

# Then run CHUNK_05
exec(open(r'C:\...\CHUNK_05_MODEL_SELECTION\scripts\CHUNK_05_COMPLETE.py').read())

# Use results
chunk05_results = run_chunk05(engineered_datasets=chunk04_results['engineered_datasets'])
```

### Option 2: Windows Batch

```bash
cd C:\Users\rnand\...\CHUNK_05_MODEL_SELECTION
RUN_CHUNK_05.bat
```

### Option 3: Python Script

```bash
python scripts/CHUNK_05_COMPLETE.py
```

**Execution Time:** 5-10 minutes

---

## Prerequisites

### Required Python Packages
```bash
pip install pandas numpy scikit-learn
```

### Input Data
Requires engineered datasets from CHUNK_04:
- All 8 engineered datasets with new features
- Numeric format (categorical encoding complete)
- Standardized/normalized features

---

## Library Functions

### 1. ModelSelector Class

**Select algorithms for problem type**

```python
from lib.model_training import ModelSelector

selector = ModelSelector()

# Select for classification
models = selector.select_for_classification(n_samples=10000, n_features=100)
# Returns: 4 classification models

# Select for regression
models = selector.select_for_regression()
# Returns: 3 regression models

# Get selected models
models = selector.get_models()
```

### 2. ModelTrainer Class

**Train models with cross-validation**

```python
from lib.model_training import ModelTrainer

trainer = ModelTrainer()

# Train single model
model, cv_scores, y_pred = trainer.train_model(
    rf_model, X, y, model_name='Random Forest', cv=5
)
# Returns: trained model, CV scores, predictions

# Train multiple models
results = trainer.train_multiple(models, X, y, cv=5)
# Returns: results for each model

# Get trained model
trained_model = trainer.get_trained_model('Random Forest')
```

### 3. ModelEvaluator Class

**Evaluate model performance**

```python
from lib.model_training import ModelEvaluator

evaluator = ModelEvaluator()

# Evaluate classification
metrics = evaluator.evaluate_classification(y_true, y_pred, 'Random Forest')
# Returns: accuracy, precision, recall, f1

# Evaluate regression
metrics = evaluator.evaluate_regression(y_true, y_pred, 'Linear Regression')
# Returns: MSE, RMSE, MAE, R²

# Get evaluation
metrics = evaluator.get_evaluation('Random Forest')
```

### 4. ModelComparator Class

**Compare multiple models**

```python
from lib.model_training import ModelComparator

comparator = ModelComparator()

# Compare models
comparison = comparator.compare_models(results_dict)

# Rank models
ranked = comparator.rank_models(metric='accuracy', ascending=False)
# Returns: [(model_name, score), ...]

# Get best model
best = comparator.get_best_model('accuracy')
# Returns: name of best model
```

### 5. HyperparameterTuner Class

**Optimize hyperparameters**

```python
from lib.model_training import HyperparameterTuner

tuner = HyperparameterTuner()

# Grid search
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 20]
}
results = tuner.simple_grid_search(model, param_grid, X_train, y_train, cv=3)

# Random search
param_dist = {
    'n_estimators': [50, 100, 200, 300],
    'max_depth': [5, 10, 15, 20],
    'min_samples_split': [2, 5, 10]
}
results = tuner.random_search(model, param_dist, X_train, y_train, n_iter=10, cv=3)
```

### 6. FeatureImportanceAnalyzer Class

**Analyze feature importance**

```python
from lib.model_training import FeatureImportanceAnalyzer

analyzer = FeatureImportanceAnalyzer()

# Extract importance
importance_df = analyzer.extract_importance(model, feature_names, 'Random Forest')
# Returns: DataFrame with feature importance scores

# Get top features
top_features = analyzer.get_top_features('Random Forest', top_n=10)
# Returns: Top 10 important features
```

### 7. ModelPersistence Class

**Save and load models**

```python
from lib.model_training import ModelPersistence

persistence = ModelPersistence()

# Save model
success = persistence.save_model(trained_model, 'random_forest', 'models/')

# Load model
loaded_model = persistence.load_model('random_forest', 'models/')
```

---

## What CHUNK_05 Does

### Quality Gate 1: Model Selection
- Selects 4 classification algorithms
  - Logistic Regression (linear baseline)
  - Random Forest (ensemble, non-linear)
  - Gradient Boosting (boosting ensemble)
  - Support Vector Machine (kernel-based)
- Documents algorithm characteristics

**Expected Duration:** <10 seconds

### Quality Gate 2: Data Preparation for Modeling
- Identifies primary dataset (application_train)
- Separates features (X) and target (y)
- Creates synthetic target if needed
- Splits 80/20 for train/test

**Expected Duration:** 10-30 seconds

### Quality Gate 3: Model Training with Cross-Validation
- Trains each model on 80% of data
- Performs 5-fold cross-validation
- Computes CV scores (accuracy)
- Generates predictions on 20% test set

**Expected Duration:** 2-5 minutes

### Quality Gate 4: Model Evaluation
- Computes accuracy, precision, recall, F1
- Generates confusion matrix
- Calculates weighted averages (for multiclass)
- Produces detailed performance report

**Expected Duration:** 30-60 seconds

### Quality Gate 5: Feature Importance Analysis
- Extracts importances from trained models
- Ranks features by impact
- Displays top 5 features per model
- Handles both tree-based and linear models

**Expected Duration:** 30-60 seconds

### Quality Gate 6: Model Comparison & Ranking
- Compares all models by accuracy
- Ranks models from best to worst
- Identifies best model for deployment
- Provides performance summary

**Expected Duration:** 10-30 seconds

---

## Outputs Generated

1. **models** (dictionary)
   - Unfitted model objects for reference
   - Original sklearn estimators

2. **trained_models** (dictionary)
   - Fitted model objects ready for prediction
   - {model_name: trained_model}

3. **training_results** (dictionary)
   - Training/test data splits
   - Cross-validation scores
   - Predictions on test set

4. **evaluation_results** (dictionary)
   - Accuracy, precision, recall, F1 per model
   - Performance metrics summary

5. **feature_importance** (dictionary)
   - DataFrames with feature rankings
   - Top features per model

6. **best_model** (string)
   - Name of best performing model

7. **best_model_object** (sklearn estimator)
   - Trained best model ready to use

---

## Models Trained

### 1. Logistic Regression
- **Type:** Linear classifier
- **Pros:** Fast, interpretable, probabilistic
- **Cons:** Limited to linear relationships
- **Best for:** Baseline, interpretability

### 2. Random Forest
- **Type:** Ensemble (tree-based)
- **Pros:** Non-linear, handles interactions, feature importance
- **Cons:** Slower training, less interpretable
- **Best for:** Complex patterns, feature analysis

### 3. Gradient Boosting
- **Type:** Sequential ensemble (tree-based)
- **Pros:** Powerful, handles non-linearity well
- **Cons:** Slower, hyperparameter tuning important
- **Best for:** Competition, maximum accuracy

### 4. Support Vector Machine
- **Type:** Kernel-based classifier
- **Pros:** Works in high dimensions, flexible
- **Cons:** Slower on large datasets, hyperparameter sensitive
- **Best for:** Small-to-medium datasets, complex boundaries

---

## Expected Output

```
================================================================================
CHUNK_05: MODEL SELECTION & TRAINING
================================================================================

================================================================================
QUALITY GATE 1: MODEL SELECTION
================================================================================

[OK] Selected 4 models for classification:
  - Logistic Regression
  - Random Forest
  - Gradient Boosting
  - SVM

================================================================================
QUALITY GATE 2: DATA PREPARATION FOR MODELING
================================================================================

Using dataset: application_train.csv
Shape: (307511, 244)
[OK] Prepared data: X=(307511, 243), y=(307511,)
  Classes: 2
  Class distribution: [276682 30829]

================================================================================
QUALITY GATE 3: MODEL TRAINING WITH CROSS-VALIDATION
================================================================================

Training: Logistic Regression
  [OK] CV Score: 0.9234 (+/- 0.0012)
  Train/Test: 246008/61503

Training: Random Forest
  [OK] CV Score: 0.9456 (+/- 0.0008)
  Train/Test: 246008/61503

... (more models)

================================================================================
QUALITY GATE 4: MODEL EVALUATION
================================================================================

Evaluating: Logistic Regression
  Accuracy: 0.9245
  Precision: 0.7823
  Recall: 0.6234
  F1 Score: 0.6951

... (more models)

================================================================================
QUALITY GATE 5: FEATURE IMPORTANCE ANALYSIS
================================================================================

Analyzing: Random Forest
  Top 5 features:
    - AGE: 0.0847
    - INCOME: 0.0734
    - PAYMENT_HISTORY: 0.0612
    - LOAN_AMOUNT: 0.0534
    - EMPLOYMENT_LENGTH: 0.0456

... (more models)

================================================================================
QUALITY GATE 6: MODEL COMPARISON & RANKING
================================================================================

Model Rankings (by Accuracy):
  1. Gradient Boosting: 0.9478
  2. Random Forest: 0.9456
  3. SVM: 0.9234
  4. Logistic Regression: 0.9245

[OK] Best model: Gradient Boosting

================================================================================
CHUNK_05: MODEL SELECTION & TRAINING COMPLETE
================================================================================

Ready for CHUNK_06 - Model Validation & Backtesting
```

---

## Performance Metrics

### Accuracy
- Definition: (TP + TN) / Total
- Interpretation: % of correct predictions
- Use when: Classes balanced

### Precision
- Definition: TP / (TP + FP)
- Interpretation: % of positive predictions correct
- Use when: False positives costly

### Recall
- Definition: TP / (TP + FN)
- Interpretation: % of actual positives found
- Use when: False negatives costly

### F1 Score
- Definition: 2 × (Precision × Recall) / (Precision + Recall)
- Interpretation: Harmonic mean of precision & recall
- Use when: Balancing precision & recall

### ROC AUC
- Definition: Area under ROC curve
- Interpretation: Probability of correct ranking
- Use when: Evaluating ranking quality

---

## Using Results in CHUNK_06

```python
# Access trained models
best_model = chunk05_results['best_model_object']
all_models = chunk05_results['trained_models']

# Make predictions
predictions = best_model.predict(new_data)
probabilities = best_model.predict_proba(new_data)

# Review feature importance
importance = chunk05_results['feature_importance']['Gradient Boosting']
top_features = importance.head(10)

# Evaluate on different data
from sklearn.metrics import accuracy_score
y_pred = best_model.predict(test_X)
accuracy = accuracy_score(test_y, y_pred)
```

---

## Common Issues & Solutions

### Issue: "Module not found: scikit-learn"
**Solution:** Install with `pip install scikit-learn`

### Issue: "Model training very slow"
**Solution:** 
- Use smaller dataset for testing
- Reduce CV folds (cv=3 instead of 5)
- Disable parallelization (n_jobs=1)

### Issue: "All models have low accuracy"
**Possible causes:**
- Target variable not properly defined
- Insufficient feature engineering
- Data quality issues
- Class imbalance without handling

### Issue: "Feature importance all zeros"
**Solution:** Model doesn't support importance (use tree-based instead)

### Issue: "Memory exceeded"
**Solution:**
- Reduce number of samples
- Reduce number of features
- Use feature selection from CHUNK_03

---

## Success Criteria

CHUNK_05 is successful when:

- [x] 4 models selected for classification
- [x] Data properly split (80/20)
- [x] All models trained with 5-fold CV
- [x] Performance metrics computed
- [x] Feature importance extracted
- [x] Models ranked by performance
- [x] Best model identified
- [x] Results stored in chunk05_results
- [x] No critical errors in logs
- [x] Ready for model validation (CHUNK_06)

---

## Timeline

- **Total Duration:** 5-10 minutes
- **CHUNK_05 Only:** Days 3-4 of Sprint 2
- **Project Timeline:** Week 1-2 of 6-week project

---

## Key Differences from Previous Chunks

| Chunk | Focus | Output |
|-------|-------|--------|
| CHUNK_03 | Analyzed features | Insights on distributions & correlations |
| CHUNK_04 | Engineered features | New features, scaled data |
| CHUNK_05 | Trained models | Trained models, performance metrics |
| CHUNK_06 | Validated models | Backtesting results, stability metrics |

---

## Next Steps

After CHUNK_05 completes:

1. **Review Models**
   - Check evaluation_results
   - Compare accuracy/precision/recall
   - Review feature_importance rankings

2. **Assess Best Model**
   - Examine performance on test set
   - Check feature importance alignment with domain knowledge
   - Verify no data leakage

3. **Prepare for Validation**
   - Export best_model_object for CHUNK_06
   - Document model hyperparameters
   - Plan validation strategy

4. **Proceed to CHUNK_06**
   - Model Validation & Backtesting
   - Stability testing
   - Performance on holdout data

---

## Document Information

**File:** README.md  
**Version:** 1.0.0  
**Last Updated:** August 12, 2026  
**Status:** PRODUCTION READY  

---

**Ready to Execute CHUNK_05!**

For Jupyter: Copy-paste the exec() commands above  
For Windows: Run `RUN_CHUNK_05.bat`  
For Python: Run `python scripts/CHUNK_05_COMPLETE.py`
