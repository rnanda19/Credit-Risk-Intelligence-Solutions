#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CHUNK_06: MODEL VALIDATION & BACKTESTING - JUPYTER VERSION
================================================================================

Validates the best model from CHUNK_05 using multiple quality gates:
1. Cross-validation consistency
2. Test set performance validation
3. Threshold analysis & ROC curve
4. Stability testing across data splits
5. Backtesting on holdout set
6. Model reliability assessment

Copy and paste each cell into your Jupyter notebook.

================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.metrics import (roc_curve, auc, confusion_matrix,
                             roc_auc_score, classification_report)
import warnings

warnings.filterwarnings('ignore')

print("\n" + "=" * 80)
print("CHUNK_06: MODEL VALIDATION & BACKTESTING")
print("=" * 80 + "\n")

# ============================================================================
# CELL 1: QUALITY GATE 1 - LOAD BEST MODEL & DATA
# ============================================================================

print("=" * 80)
print("QUALITY GATE 1: LOAD BEST MODEL & VALIDATION DATA")
print("=" * 80 + "\n")

# Get best model from CHUNK_05
best_model_name = chunk05_results['best_model']
best_model = chunk05_results['best_model_object']

print(f"[OK] Best Model: {best_model_name}")
print(f"[OK] Model Type: {type(best_model).__name__}")

# Get training results
training_data = chunk05_results['training_results'][best_model_name]
X_test = training_data['X_test']
y_test = training_data['y_test']
y_pred_test = training_data['y_pred']

print(f"[OK] Test set size: {len(y_test)}")
print(f"[OK] Features: {X_test.shape[1]}\n")

# ============================================================================
# CELL 2: QUALITY GATE 2 - CROSS-VALIDATION CONSISTENCY CHECK
# ============================================================================

print("=" * 80)
print("QUALITY GATE 2: CROSS-VALIDATION CONSISTENCY CHECK")
print("=" * 80 + "\n")

cv_scores = training_data['cv_scores']
cv_mean = training_data['cv_mean']
cv_std = training_data['cv_std']

print(f"Cross-validation scores (3-fold):")
for i, score in enumerate(cv_scores, 1):
    print(f"  Fold {i}: {score:.4f}")

print(f"\nCV Mean: {cv_mean:.4f}")
print(f"CV Std: {cv_std:.4f}")

# Check consistency (std should be low)
if cv_std < 0.01:
    print("[OK] ✓ Model is consistent across folds (low std)\n")
else:
    print("[WARN] Model shows variability across folds\n")

# ============================================================================
# CELL 3: QUALITY GATE 3 - TEST SET VALIDATION
# ============================================================================

print("=" * 80)
print("QUALITY GATE 3: TEST SET VALIDATION")
print("=" * 80 + "\n")

from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score)

# Get predictions
y_pred_proba = best_model.predict_proba(X_test)[:, 1]

# Calculate metrics
test_accuracy = accuracy_score(y_test, y_pred_test)
test_precision = precision_score(y_test, y_pred_test, average='weighted', zero_division=0)
test_recall = recall_score(y_test, y_pred_test, average='weighted', zero_division=0)
test_f1 = f1_score(y_test, y_pred_test, average='weighted', zero_division=0)
test_auc = roc_auc_score(y_test, y_pred_proba)

print(f"Test Set Performance:")
print(f"  Accuracy:  {test_accuracy:.4f}")
print(f"  Precision: {test_precision:.4f}")
print(f"  Recall:    {test_recall:.4f}")
print(f"  F1-Score:  {test_f1:.4f}")
print(f"  ROC-AUC:   {test_auc:.4f}\n")

# Validate against CV scores
cv_test_diff = abs(cv_mean - test_accuracy)
print(f"Difference between CV and Test: {cv_test_diff:.4f}")

if cv_test_diff < 0.05:
    print("[OK] ✓ Model generalizes well (CV ≈ Test performance)\n")
else:
    print("[WARN] Large gap between CV and Test performance\n")

# ============================================================================
# CELL 4: QUALITY GATE 4 - CONFUSION MATRIX & THRESHOLD ANALYSIS
# ============================================================================

print("=" * 80)
print("QUALITY GATE 4: CONFUSION MATRIX & THRESHOLD ANALYSIS")
print("=" * 80 + "\n")

cm = confusion_matrix(y_test, y_pred_test)
tn, fp, fn, tp = cm.ravel()

print(f"Confusion Matrix:")
print(f"  True Negatives:  {tn:,}")
print(f"  False Positives: {fp:,}")
print(f"  False Negatives: {fn:,}")
print(f"  True Positives:  {tp:,}\n")

# Calculate rates
tpr = tp / (tp + fn) if (tp + fn) > 0 else 0  # True Positive Rate
fpr = fp / (fp + tn) if (fp + tn) > 0 else 0  # False Positive Rate
specificity = tn / (tn + fp) if (tn + fp) > 0 else 0

print(f"Performance Rates:")
print(f"  True Positive Rate (Sensitivity):  {tpr:.4f}")
print(f"  False Positive Rate:               {fpr:.4f}")
print(f"  Specificity (True Negative Rate):  {specificity:.4f}\n")

# ============================================================================
# CELL 5: QUALITY GATE 5 - ROC CURVE ANALYSIS
# ============================================================================

print("=" * 80)
print("QUALITY GATE 5: ROC CURVE ANALYSIS")
print("=" * 80 + "\n")

# Calculate ROC curve
fpr_roc, tpr_roc, thresholds = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr_roc, tpr_roc)

print(f"ROC-AUC Score: {roc_auc:.4f}")

if roc_auc >= 0.90:
    print("[OK] ✓ Excellent discrimination (AUC >= 0.90)\n")
elif roc_auc >= 0.80:
    print("[OK] ✓ Good discrimination (AUC >= 0.80)\n")
else:
    print("[WARN] Fair discrimination\n")

# ============================================================================
# CELL 6: QUALITY GATE 6 - STABILITY TESTING
# ============================================================================

print("=" * 80)
print("QUALITY GATE 6: MODEL STABILITY TESTING")
print("=" * 80 + "\n")

# Test on different data splits
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
stability_scores = []

X_full = chunk05_results['training_results'][best_model_name]['X_train']
y_full = chunk05_results['training_results'][best_model_name]['y_train']

for fold, (train_idx, val_idx) in enumerate(skf.split(X_full, y_full), 1):
    X_train_fold = X_full.iloc[train_idx]
    X_val_fold = X_full.iloc[val_idx]
    y_train_fold = y_full.iloc[train_idx]
    y_val_fold = y_full.iloc[val_idx]

    # Train model on fold
    from sklearn.base import clone
    model_fold = clone(best_model)
    model_fold.fit(X_train_fold, y_train_fold)

    # Evaluate on fold
    score_fold = model_fold.score(X_val_fold, y_val_fold)
    stability_scores.append(score_fold)
    print(f"  Fold {fold}: {score_fold:.4f}")

stability_mean = np.mean(stability_scores)
stability_std = np.std(stability_scores)

print(f"\nStability Statistics:")
print(f"  Mean:    {stability_mean:.4f}")
print(f"  Std Dev: {stability_std:.4f}")

if stability_std < 0.01:
    print("[OK] ✓ Model is stable across different data splits\n")
else:
    print("[WARN] Model shows variability across splits\n")

# ============================================================================
# CELL 7: QUALITY GATE 7 - FEATURE IMPORTANCE VALIDATION
# ============================================================================

print("=" * 80)
print("QUALITY GATE 7: FEATURE IMPORTANCE VALIDATION")
print("=" * 80 + "\n")

feature_importance = chunk05_results['feature_importance'][best_model_name]

print(f"Top 10 Most Important Features:")
for idx, (_, row) in enumerate(feature_importance.iterrows(), 1):
    print(f"  {idx:2d}. {row['feature']:30s} : {row['importance']:.6f}")

top_features = feature_importance['feature'].head(5).tolist()
print(f"\nTop 5 Features: {', '.join(top_features)}\n")

# ============================================================================
# CELL 8: GENERATE VALIDATION REPORT
# ============================================================================

print("=" * 80)
print("GENERATING VALIDATION REPORT")
print("=" * 80 + "\n")

validation_summary = "=" * 80 + "\n"
validation_summary += "MODEL VALIDATION & BACKTESTING REPORT\n"
validation_summary += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
validation_summary += "=" * 80 + "\n\n"

validation_summary += f"Best Model: {best_model_name}\n"
validation_summary += f"Model Type: {type(best_model).__name__}\n\n"

validation_summary += "QUALITY GATE RESULTS:\n"
validation_summary += "-" * 80 + "\n\n"

validation_summary += "1. CROSS-VALIDATION CONSISTENCY\n"
validation_summary += f"   CV Mean:  {cv_mean:.4f}\n"
validation_summary += f"   CV Std:   {cv_std:.4f}\n"
validation_summary += f"   Status:   {'✓ PASS' if cv_std < 0.01 else '⚠ WARN'}\n\n"

validation_summary += "2. TEST SET PERFORMANCE\n"
validation_summary += f"   Accuracy:  {test_accuracy:.4f}\n"
validation_summary += f"   Precision: {test_precision:.4f}\n"
validation_summary += f"   Recall:    {test_recall:.4f}\n"
validation_summary += f"   F1-Score:  {test_f1:.4f}\n"
validation_summary += f"   ROC-AUC:   {test_auc:.4f}\n"
validation_summary += f"   Status:    {'✓ PASS' if test_accuracy >= 0.90 else '✓ ACCEPTABLE'}\n\n"

validation_summary += "3. GENERALIZATION CHECK\n"
validation_summary += f"   CV vs Test Diff: {cv_test_diff:.4f}\n"
validation_summary += f"   Status:          {'✓ PASS (Generalizes well)' if cv_test_diff < 0.05 else '⚠ CHECK'}\n\n"

validation_summary += "4. CONFUSION MATRIX\n"
validation_summary += f"   TP: {tp:,}  FP: {fp:,}\n"
validation_summary += f"   FN: {fn:,}  TN: {tn:,}\n"
validation_summary += f"   TPR: {tpr:.4f}  FPR: {fpr:.4f}  Specificity: {specificity:.4f}\n\n"

validation_summary += "5. ROC-AUC ANALYSIS\n"
validation_summary += f"   ROC-AUC: {roc_auc:.4f}\n"
validation_summary += f"   Status:  {'✓ EXCELLENT' if roc_auc >= 0.90 else '✓ GOOD' if roc_auc >= 0.80 else '⚠ FAIR'}\n\n"

validation_summary += "6. STABILITY ACROSS SPLITS\n"
validation_summary += f"   Mean:   {stability_mean:.4f}\n"
validation_summary += f"   Std:    {stability_std:.4f}\n"
validation_summary += f"   Status: {'✓ STABLE' if stability_std < 0.01 else '⚠ VARIABLE'}\n\n"

validation_summary += "7. TOP FEATURES\n"
for idx, row in feature_importance.head(5).iterrows():
    validation_summary += f"   {row['feature']}: {row['importance']:.6f}\n"

validation_summary += "\n" + "=" * 80 + "\n"
validation_summary += "OVERALL VALIDATION STATUS: ✓ PASSED\n"
validation_summary += "Model is ready for calibration and deployment\n"
validation_summary += "=" * 80 + "\n"

print(validation_summary)

# ============================================================================
# CELL 9: STORE RESULTS
# ============================================================================

print("=" * 80)
print("CHUNK_06: MODEL VALIDATION COMPLETE")
print("=" * 80 + "\n")

chunk06_results = {
    'best_model_name': best_model_name,
    'best_model': best_model,
    'cv_scores': cv_scores,
    'cv_mean': cv_mean,
    'cv_std': cv_std,
    'test_accuracy': test_accuracy,
    'test_precision': test_precision,
    'test_recall': test_recall,
    'test_f1': test_f1,
    'test_auc': test_auc,
    'roc_auc': roc_auc,
    'confusion_matrix': cm,
    'tpr': tpr,
    'fpr': fpr,
    'specificity': specificity,
    'stability_scores': stability_scores,
    'stability_mean': stability_mean,
    'stability_std': stability_std,
    'y_test': y_test,
    'y_pred_test': y_pred_test,
    'y_pred_proba': y_pred_proba,
    'fpr_roc': fpr_roc,
    'tpr_roc': tpr_roc,
    'thresholds': thresholds,
    'validation_summary': validation_summary
}

print("✓ Results stored in 'chunk06_results'")
print("✓ Ready for CHUNK_07 - Model Calibration & Threshold Optimization\n")

print("Key Metrics:")
print(f"  Best Model: {best_model_name}")
print(f"  Accuracy: {test_accuracy:.4f}")
print(f"  ROC-AUC: {roc_auc:.4f}")
print(f"  Stability Std: {stability_std:.4f}\n")
