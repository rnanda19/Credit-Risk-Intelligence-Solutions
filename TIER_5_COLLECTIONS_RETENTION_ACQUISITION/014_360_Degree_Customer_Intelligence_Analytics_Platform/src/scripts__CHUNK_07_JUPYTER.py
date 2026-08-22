#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CHUNK_07: MODEL CALIBRATION & THRESHOLD OPTIMIZATION - JUPYTER VERSION
================================================================================

Optimizes decision threshold and calibrates model predictions:
1. Analyze current threshold (0.5) performance
2. Test alternative thresholds
3. Calculate cost-benefit for each threshold
4. Calibrate probability predictions
5. Generate business recommendations
6. Determine optimal deployment threshold

Copy and paste each cell into your Jupyter notebook.

================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.calibration import calibration_curve
import warnings

warnings.filterwarnings('ignore')

print("\n" + "=" * 80)
print("CHUNK_07: MODEL CALIBRATION & THRESHOLD OPTIMIZATION")
print("=" * 80 + "\n")

# ============================================================================
# CELL 1: QUALITY GATE 1 - LOAD VALIDATION RESULTS
# ============================================================================

print("=" * 80)
print("QUALITY GATE 1: LOAD VALIDATION RESULTS")
print("=" * 80 + "\n")

best_model = chunk06_results['best_model']
y_test = chunk06_results['y_test']
y_pred_proba = chunk06_results['y_pred_proba']

print(f"[OK] Best Model: {chunk06_results['best_model_name']}")
print(f"[OK] Test set size: {len(y_test)}")
print(f"[OK] Prediction probabilities available: {len(y_pred_proba)}")
print(f"[OK] Probability range: [{y_pred_proba.min():.4f}, {y_pred_proba.max():.4f}]\n")

# ============================================================================
# CELL 2: QUALITY GATE 2 - CURRENT THRESHOLD ANALYSIS (0.5)
# ============================================================================

print("=" * 80)
print("QUALITY GATE 2: CURRENT THRESHOLD ANALYSIS (0.5)")
print("=" * 80 + "\n")

current_threshold = 0.5
y_pred_current = (y_pred_proba >= current_threshold).astype(int)

from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

cm_current = confusion_matrix(y_test, y_pred_current)
tn_c, fp_c, fn_c, tp_c = cm_current.ravel()

acc_current = accuracy_score(y_test, y_pred_current)
prec_current = precision_score(y_test, y_pred_current, zero_division=0)
rec_current = recall_score(y_test, y_pred_current, zero_division=0)
f1_current = f1_score(y_test, y_pred_current, zero_division=0)

print(f"Current Threshold: {current_threshold}")
print(f"\nConfusion Matrix:")
print(f"  TP: {tp_c:6d}  FP: {fp_c:6d}")
print(f"  FN: {fn_c:6d}  TN: {tn_c:6d}")

print(f"\nPerformance Metrics:")
print(f"  Accuracy:  {acc_current:.4f}")
print(f"  Precision: {prec_current:.4f}")
print(f"  Recall:    {rec_current:.4f}")
print(f"  F1-Score:  {f1_current:.4f}")

print(f"\nRates:")
print(f"  True Positive Rate (Sensitivity):  {tp_c / (tp_c + fn_c):.4f}")
print(f"  False Positive Rate:               {fp_c / (fp_c + tn_c):.4f}")
print(f"  Specificity:                       {tn_c / (tn_c + fp_c):.4f}\n")

# ============================================================================
# CELL 3: QUALITY GATE 3 - THRESHOLD SWEEP ANALYSIS
# ============================================================================

print("=" * 80)
print("QUALITY GATE 3: THRESHOLD SWEEP ANALYSIS")
print("=" * 80 + "\n")

thresholds_to_test = np.arange(0.1, 1.0, 0.05)
threshold_results = []

for thresh in thresholds_to_test:
    y_pred_thresh = (y_pred_proba >= thresh).astype(int)
    cm_thresh = confusion_matrix(y_test, y_pred_thresh)

    if len(cm_thresh) == 2 and cm_thresh.shape == (2, 2):
        tn, fp, fn, tp = cm_thresh.ravel()
    else:
        tn, fp, fn, tp = 0, 0, len(y_test), 0

    acc = accuracy_score(y_test, y_pred_thresh)
    prec = precision_score(y_test, y_pred_thresh, zero_division=0)
    rec = recall_score(y_test, y_pred_thresh, zero_division=0)
    f1 = f1_score(y_test, y_pred_thresh, zero_division=0)

    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0

    # Cost calculation (example: FP cost = 1, FN cost = 5)
    fp_cost = 1.0  # Cost of false alarm
    fn_cost = 5.0  # Cost of missing default (5x more expensive)
    total_cost = (fp * fp_cost) + (fn * fn_cost)

    threshold_results.append({
        'threshold': thresh,
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'f1': f1,
        'tp': tp,
        'fp': fp,
        'tn': tn,
        'fn': fn,
        'tpr': tpr,
        'fpr': fpr,
        'total_cost': total_cost
    })

results_df = pd.DataFrame(threshold_results)

print("Threshold Performance Sweep:")
print(results_df.to_string(index=False))
print()

# ============================================================================
# CELL 4: QUALITY GATE 4 - OPTIMAL THRESHOLD SELECTION
# ============================================================================

print("=" * 80)
print("QUALITY GATE 4: OPTIMAL THRESHOLD SELECTION")
print("=" * 80 + "\n")

# Find threshold with lowest total cost (FP + 5*FN)
min_cost_idx = results_df['total_cost'].idxmin()
optimal_threshold = results_df.loc[min_cost_idx, 'threshold']
optimal_cost = results_df.loc[min_cost_idx, 'total_cost']

print(f"Cost-Benefit Analysis (FP=1, FN=5):")
print(f"  Current threshold (0.5): Cost = {current_threshold:.1f}")
print(f"  Optimal threshold: {optimal_threshold:.2f}")
print(f"  Total cost at optimal: {optimal_cost:.0f}\n")

# Show metrics at optimal threshold
opt_row = results_df.loc[min_cost_idx]
print(f"Metrics at optimal threshold ({optimal_threshold:.2f}):")
print(f"  Accuracy:  {opt_row['accuracy']:.4f}")
print(f"  Precision: {opt_row['precision']:.4f}")
print(f"  Recall:    {opt_row['recall']:.4f}")
print(f"  F1-Score:  {opt_row['f1']:.4f}")
print(f"  TPR:       {opt_row['tpr']:.4f}")
print(f"  FPR:       {opt_row['fpr']:.4f}\n")

# Improvement
cost_improvement = ((current_threshold - optimal_cost) / current_threshold) * 100
print(f"Cost improvement: {cost_improvement:.1f}%\n")

# ============================================================================
# CELL 5: QUALITY GATE 5 - CALIBRATION CURVE
# ============================================================================

print("=" * 80)
print("QUALITY GATE 5: PROBABILITY CALIBRATION ANALYSIS")
print("=" * 80 + "\n")

# Calculate calibration curve
prob_true, prob_pred = calibration_curve(y_test, y_pred_proba, n_bins=10)

print("Calibration Curve (10 bins):")
print("Predicted Prob | Actual Prob | Bin Size")
print("-" * 45)

for i in range(len(prob_true)):
    bin_size = np.sum((y_pred_proba >= i*0.1) & (y_pred_proba < (i+1)*0.1))
    print(f"    {prob_pred[i]:.3f}     |    {prob_true[i]:.3f}     |   {bin_size:6d}")

# Check calibration quality
calibration_error = np.mean(np.abs(prob_true - prob_pred))
print(f"\nMean Absolute Calibration Error: {calibration_error:.4f}")

if calibration_error < 0.05:
    print("[OK] ✓ Model probabilities are well-calibrated\n")
else:
    print("[WARN] Model probabilities may need recalibration\n")

# ============================================================================
# CELL 6: QUALITY GATE 6 - BUSINESS RECOMMENDATIONS
# ============================================================================

print("=" * 80)
print("QUALITY GATE 6: BUSINESS RECOMMENDATIONS")
print("=" * 80 + "\n")

# Get all candidate thresholds with good F1
good_f1_mask = results_df['f1'] >= 0.80
good_thresholds = results_df[good_f1_mask].sort_values('total_cost')

print("Top 5 Threshold Recommendations (by cost):\n")

for rank, (idx, row) in enumerate(good_thresholds.head(5).iterrows(), 1):
    thresh = row['threshold']
    print(f"{rank}. Threshold: {thresh:.2f}")
    print(f"   Accuracy:  {row['accuracy']:.4f}")
    print(f"   Precision: {row['precision']:.4f} (of predicted defaults, {row['precision']*100:.1f}% correct)")
    print(f"   Recall:    {row['recall']:.4f} (catch {row['recall']*100:.1f}% of defaults)")
    print(f"   F1-Score:  {row['f1']:.4f}")
    print(f"   TP: {row['tp']:.0f} | FP: {row['fp']:.0f} | FN: {row['fn']:.0f}")
    print(f"   Cost:      {row['total_cost']:.0f}")
    print()

# ============================================================================
# CELL 7: QUALITY GATE 7 - THRESHOLD COMPARISON TABLE
# ============================================================================

print("=" * 80)
print("QUALITY GATE 7: THRESHOLD COMPARISON")
print("=" * 80 + "\n")

comparison_thresholds = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
comparison_results = []

for thresh in comparison_thresholds:
    row = results_df[results_df['threshold'] == thresh]
    if len(row) > 0:
        comparison_results.append({
            'Threshold': f"{thresh:.2f}",
            'Accuracy': f"{row['accuracy'].values[0]:.4f}",
            'Precision': f"{row['precision'].values[0]:.4f}",
            'Recall': f"{row['recall'].values[0]:.4f}",
            'F1': f"{row['f1'].values[0]:.4f}",
            'Cost': f"{row['total_cost'].values[0]:.0f}"
        })

comparison_df = pd.DataFrame(comparison_results)
print(comparison_df.to_string(index=False))
print()

# ============================================================================
# CELL 8: GENERATE CALIBRATION REPORT
# ============================================================================

print("=" * 80)
print("GENERATING CALIBRATION REPORT")
print("=" * 80 + "\n")

calibration_summary = "=" * 80 + "\n"
calibration_summary += "MODEL CALIBRATION & THRESHOLD OPTIMIZATION REPORT\n"
calibration_summary += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
calibration_summary += "=" * 80 + "\n\n"

calibration_summary += f"Best Model: {chunk06_results['best_model_name']}\n\n"

calibration_summary += "CURRENT THRESHOLD PERFORMANCE (0.5000):\n"
calibration_summary += "-" * 80 + "\n"
calibration_summary += f"Accuracy:  {acc_current:.4f}\n"
calibration_summary += f"Precision: {prec_current:.4f}\n"
calibration_summary += f"Recall:    {rec_current:.4f}\n"
calibration_summary += f"F1-Score:  {f1_current:.4f}\n"
calibration_summary += f"TP: {tp_c} | FP: {fp_c} | FN: {fn_c} | TN: {tn_c}\n"
calibration_summary += f"Estimated Cost (FP=1, FN=5): {(fp_c * 1.0) + (fn_c * 5.0):.0f}\n\n"

calibration_summary += "OPTIMAL THRESHOLD PERFORMANCE ({:.4f}):\n".format(optimal_threshold)
calibration_summary += "-" * 80 + "\n"
calibration_summary += f"Accuracy:  {opt_row['accuracy']:.4f}\n"
calibration_summary += f"Precision: {opt_row['precision']:.4f}\n"
calibration_summary += f"Recall:    {opt_row['recall']:.4f}\n"
calibration_summary += f"F1-Score:  {opt_row['f1']:.4f}\n"
calibration_summary += f"TP: {opt_row['tp']:.0f} | FP: {opt_row['fp']:.0f} | FN: {opt_row['fn']:.0f} | TN: {opt_row['tn']:.0f}\n"
calibration_summary += f"Estimated Cost (FP=1, FN=5): {opt_row['total_cost']:.0f}\n\n"

calibration_summary += "CALIBRATION QUALITY:\n"
calibration_summary += "-" * 80 + "\n"
calibration_summary += f"Mean Absolute Calibration Error: {calibration_error:.4f}\n"
calibration_summary += f"Status: {'✓ WELL-CALIBRATED' if calibration_error < 0.05 else '⚠ NEEDS TUNING'}\n\n"

calibration_summary += "DEPLOYMENT RECOMMENDATION:\n"
calibration_summary += "-" * 80 + "\n"
calibration_summary += f"Recommended Threshold: {optimal_threshold:.4f}\n"
calibration_summary += f"Change from current: {(optimal_threshold - current_threshold):+.4f}\n"
calibration_summary += f"Expected cost reduction: {cost_improvement:.1f}%\n\n"

calibration_summary += "=" * 80 + "\n"

print(calibration_summary)

# ============================================================================
# CELL 9: STORE RESULTS
# ============================================================================

print("=" * 80)
print("CHUNK_07: MODEL CALIBRATION COMPLETE")
print("=" * 80 + "\n")

chunk07_results = {
    'current_threshold': current_threshold,
    'optimal_threshold': optimal_threshold,
    'current_metrics': {
        'accuracy': acc_current,
        'precision': prec_current,
        'recall': rec_current,
        'f1': f1_current,
        'tp': tp_c,
        'fp': fp_c,
        'fn': fn_c,
        'tn': tn_c,
        'cost': (fp_c * 1.0) + (fn_c * 5.0)
    },
    'optimal_metrics': {
        'accuracy': opt_row['accuracy'],
        'precision': opt_row['precision'],
        'recall': opt_row['recall'],
        'f1': opt_row['f1'],
        'tp': opt_row['tp'],
        'fp': opt_row['fp'],
        'fn': opt_row['fn'],
        'tn': opt_row['tn'],
        'cost': opt_row['total_cost']
    },
    'threshold_results': results_df,
    'calibration_error': calibration_error,
    'prob_true': prob_true,
    'prob_pred': prob_pred,
    'calibration_summary': calibration_summary,
    'y_pred_proba': y_pred_proba,
    'best_model': best_model
}

print("✓ Results stored in 'chunk07_results'")
print("✓ Ready for CHUNK_08 - Explainability & Feature Analysis\n")

print("Key Findings:")
print(f"  Current Threshold: {current_threshold:.4f}")
print(f"  Optimal Threshold: {optimal_threshold:.4f}")
print(f"  Cost Improvement: {cost_improvement:.1f}%")
print(f"  Calibration Quality: {'✓ EXCELLENT' if calibration_error < 0.05 else '⚠ CHECK'}\n")
