#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
CHUNK_07: MODEL CALIBRATION & THRESHOLD OPTIMIZATION - COMPLETE VERSION
================================================================================

Optimizes decision threshold and calibrates model predictions:
1. Analyze current threshold (0.5) performance
2. Test alternative thresholds (0.1 to 1.0)
3. Calculate cost-benefit for each threshold
4. Calibrate probability predictions
5. Generate business recommendations
6. Determine optimal deployment threshold

USAGE IN JUPYTER:
    exec(open(r'CHUNK_07_MODEL_CALIBRATION/scripts/CHUNK_07_COMPLETE.py').read())

================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.calibration import calibration_curve
import warnings

warnings.filterwarnings('ignore')

print("\n" + "=" * 80)
print("CHUNK_07: MODEL CALIBRATION & THRESHOLD OPTIMIZATION")
print("=" * 80 + "\n")

# ============================================================================
# UTILITY CLASSES (Embedded)
# ============================================================================

class ThresholdAnalyzer:
    """Analyze different decision thresholds"""

    def __init__(self, y_true, y_pred_proba, fp_cost=1.0, fn_cost=5.0):
        self.y_true = y_true
        self.y_pred_proba = y_pred_proba
        self.fp_cost = fp_cost
        self.fn_cost = fn_cost
        self.results = []

    def analyze_thresholds(self, thresholds):
        """Analyze multiple thresholds"""
        for thresh in thresholds:
            y_pred = (self.y_pred_proba >= thresh).astype(int)
            cm = confusion_matrix(self.y_true, y_pred)

            if len(cm) == 2 and cm.shape == (2, 2):
                tn, fp, fn, tp = cm.ravel()
            else:
                tn, fp, fn, tp = 0, 0, len(self.y_true), 0

            acc = accuracy_score(self.y_true, y_pred)
            prec = precision_score(self.y_true, y_pred, zero_division=0)
            rec = recall_score(self.y_true, y_pred, zero_division=0)
            f1 = f1_score(self.y_true, y_pred, zero_division=0)

            tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
            cost = (fp * self.fp_cost) + (fn * self.fn_cost)

            self.results.append({
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
                'total_cost': cost
            })

        return pd.DataFrame(self.results)

    def get_optimal(self):
        """Get threshold with lowest cost"""
        results_df = pd.DataFrame(self.results)
        min_idx = results_df['total_cost'].idxmin()
        return results_df.loc[min_idx]


class ProbabilityCalibrator:
    """Calibrate probability predictions"""

    def __init__(self, y_true, y_pred_proba):
        self.y_true = y_true
        self.y_pred_proba = y_pred_proba

    def get_calibration_curve(self, n_bins=10):
        """Get calibration curve"""
        prob_true, prob_pred = calibration_curve(
            self.y_true, self.y_pred_proba, n_bins=n_bins
        )
        return prob_true, prob_pred

    def calculate_calibration_error(self, prob_true, prob_pred):
        """Calculate mean absolute calibration error"""
        return np.mean(np.abs(prob_true - prob_pred))


# ============================================================================
# MAIN EXECUTION FUNCTION
# ============================================================================

def run_chunk07(chunk06_results):
    """
    Execute CHUNK_07 Model Calibration & Threshold Optimization

    Args:
        chunk06_results: Dictionary with validation results from CHUNK_06

    Returns:
        Dictionary with calibration and threshold optimization results
    """

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

    print("=" * 80)
    print("QUALITY GATE 2: CURRENT THRESHOLD ANALYSIS (0.5)")
    print("=" * 80 + "\n")

    current_threshold = 0.5
    y_pred_current = (y_pred_proba >= current_threshold).astype(int)

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

    tpr_current = tp_c / (tp_c + fn_c) if (tp_c + fn_c) > 0 else 0
    fpr_current = fp_c / (fp_c + tn_c) if (fp_c + tn_c) > 0 else 0
    spec_current = tn_c / (tn_c + fp_c) if (tn_c + fp_c) > 0 else 0

    print(f"\nRates:")
    print(f"  True Positive Rate (Sensitivity):  {tpr_current:.4f}")
    print(f"  False Positive Rate:               {fpr_current:.4f}")
    print(f"  Specificity:                       {spec_current:.4f}\n")

    print("=" * 80)
    print("QUALITY GATE 3: THRESHOLD SWEEP ANALYSIS")
    print("=" * 80 + "\n")

    thresholds_to_test = np.arange(0.1, 1.0, 0.05)
    analyzer = ThresholdAnalyzer(y_test, y_pred_proba, fp_cost=1.0, fn_cost=5.0)
    results_df = analyzer.analyze_thresholds(thresholds_to_test)

    print("Threshold Performance Sweep (FP_cost=1, FN_cost=5):")
    print(results_df.to_string(index=False))
    print()

    print("=" * 80)
    print("QUALITY GATE 4: OPTIMAL THRESHOLD SELECTION")
    print("=" * 80 + "\n")

    optimal_row = analyzer.get_optimal()
    optimal_threshold = optimal_row['threshold']
    optimal_cost = optimal_row['total_cost']
    current_cost = (fp_c * 1.0) + (fn_c * 5.0)

    print(f"Cost-Benefit Analysis (FP=1, FN=5):")
    print(f"  Current threshold (0.5): Cost = {current_cost:.0f}")
    print(f"  Optimal threshold: {optimal_threshold:.2f}")
    print(f"  Total cost at optimal: {optimal_cost:.0f}\n")

    print(f"Metrics at optimal threshold ({optimal_threshold:.2f}):")
    print(f"  Accuracy:  {optimal_row['accuracy']:.4f}")
    print(f"  Precision: {optimal_row['precision']:.4f}")
    print(f"  Recall:    {optimal_row['recall']:.4f}")
    print(f"  F1-Score:  {optimal_row['f1']:.4f}")
    print(f"  TPR:       {optimal_row['tpr']:.4f}")
    print(f"  FPR:       {optimal_row['fpr']:.4f}\n")

    cost_improvement = ((current_cost - optimal_cost) / current_cost) * 100
    print(f"Cost improvement: {cost_improvement:.1f}%\n")

    print("=" * 80)
    print("QUALITY GATE 5: PROBABILITY CALIBRATION ANALYSIS")
    print("=" * 80 + "\n")

    calibrator = ProbabilityCalibrator(y_test, y_pred_proba)
    prob_true, prob_pred = calibrator.get_calibration_curve(n_bins=10)
    calibration_error = calibrator.calculate_calibration_error(prob_true, prob_pred)

    print("Calibration Curve (10 bins):")
    print("Predicted Prob | Actual Prob | Quality")
    print("-" * 45)

    for i in range(len(prob_true)):
        diff = abs(prob_true[i] - prob_pred[i])
        quality = "✓" if diff < 0.05 else "⚠"
        print(f"    {prob_pred[i]:.3f}     |    {prob_true[i]:.3f}     | {quality}")

    print(f"\nMean Absolute Calibration Error: {calibration_error:.4f}")

    if calibration_error < 0.05:
        print("[OK] ✓ Model probabilities are well-calibrated\n")
    else:
        print("[WARN] Model probabilities may need recalibration\n")

    print("=" * 80)
    print("QUALITY GATE 6: BUSINESS RECOMMENDATIONS")
    print("=" * 80 + "\n")

    good_f1_mask = results_df['f1'] >= 0.80
    good_thresholds = results_df[good_f1_mask].sort_values('total_cost')

    print("Top 5 Threshold Recommendations (by cost):\n")

    for rank, (idx, row) in enumerate(good_thresholds.head(5).iterrows(), 1):
        thresh = row['threshold']
        print(f"{rank}. Threshold: {thresh:.2f}")
        print(f"   Accuracy:  {row['accuracy']:.4f}")
        print(f"   Precision: {row['precision']:.4f}")
        print(f"   Recall:    {row['recall']:.4f}")
        print(f"   F1-Score:  {row['f1']:.4f}")
        print(f"   TP: {row['tp']:.0f} | FP: {row['fp']:.0f} | FN: {row['fn']:.0f}")
        print(f"   Cost:      {row['total_cost']:.0f}")
        print()

    print("=" * 80)
    print("QUALITY GATE 7: THRESHOLD COMPARISON")
    print("=" * 80 + "\n")

    comparison_thresholds = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
    comparison_rows = []

    for thresh in comparison_thresholds:
        row = results_df[results_df['threshold'] == thresh]
        if len(row) > 0:
            r = row.iloc[0]
            comparison_rows.append({
                'Threshold': f"{thresh:.2f}",
                'Accuracy': f"{r['accuracy']:.4f}",
                'Precision': f"{r['precision']:.4f}",
                'Recall': f"{r['recall']:.4f}",
                'F1': f"{r['f1']:.4f}",
                'Cost': f"{r['total_cost']:.0f}"
            })

    comparison_df = pd.DataFrame(comparison_rows)
    print(comparison_df.to_string(index=False))
    print()

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
    calibration_summary += f"Estimated Cost (FP=1, FN=5): {current_cost:.0f}\n\n"

    calibration_summary += "OPTIMAL THRESHOLD PERFORMANCE ({:.4f}):\n".format(optimal_threshold)
    calibration_summary += "-" * 80 + "\n"
    calibration_summary += f"Accuracy:  {optimal_row['accuracy']:.4f}\n"
    calibration_summary += f"Precision: {optimal_row['precision']:.4f}\n"
    calibration_summary += f"Recall:    {optimal_row['recall']:.4f}\n"
    calibration_summary += f"F1-Score:  {optimal_row['f1']:.4f}\n"
    calibration_summary += f"TP: {optimal_row['tp']:.0f} | FP: {optimal_row['fp']:.0f} | FN: {optimal_row['fn']:.0f} | TN: {optimal_row['tn']:.0f}\n"
    calibration_summary += f"Estimated Cost (FP=1, FN=5): {optimal_row['total_cost']:.0f}\n\n"

    calibration_summary += "CALIBRATION QUALITY:\n"
    calibration_summary += "-" * 80 + "\n"
    calibration_summary += f"Mean Absolute Calibration Error: {calibration_error:.4f}\n"
    calibration_summary += f"Status: {'✓ WELL-CALIBRATED' if calibration_error < 0.05 else '⚠ NEEDS TUNING'}\n\n"

    calibration_summary += "DEPLOYMENT RECOMMENDATION:\n"
    calibration_summary += "-" * 80 + "\n"
    calibration_summary += f"Recommended Threshold: {optimal_threshold:.4f}\n"
    calibration_summary += f"Change from current: {(optimal_threshold - current_threshold):+.4f}\n"
    calibration_summary += f"Expected cost reduction: {cost_improvement:.1f}%\n"
    calibration_summary += f"\nInterpretation:\n"
    calibration_summary += f"- Current (0.5000): Predict default if probability >= 0.5000\n"
    calibration_summary += f"- Optimal ({optimal_threshold:.4f}): Predict default if probability >= {optimal_threshold:.4f}\n"
    calibration_summary += f"- This lowers threshold, catching more defaults with acceptable false alarms\n\n"

    calibration_summary += "=" * 80 + "\n"

    print(calibration_summary)

    print("\n" + "=" * 80)
    print("CHUNK_07: MODEL CALIBRATION COMPLETE")
    print("=" * 80 + "\n")

    return {
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
            'cost': current_cost
        },
        'optimal_metrics': {
            'accuracy': float(optimal_row['accuracy']),
            'precision': float(optimal_row['precision']),
            'recall': float(optimal_row['recall']),
            'f1': float(optimal_row['f1']),
            'tp': float(optimal_row['tp']),
            'fp': float(optimal_row['fp']),
            'fn': float(optimal_row['fn']),
            'tn': float(optimal_row['tn']),
            'cost': float(optimal_row['total_cost'])
        },
        'threshold_results': results_df,
        'calibration_error': calibration_error,
        'prob_true': prob_true,
        'prob_pred': prob_pred,
        'calibration_summary': calibration_summary,
        'y_pred_proba': y_pred_proba,
        'best_model': best_model,
        'cost_improvement': cost_improvement
    }


# ============================================================================
# AUTO-RUN IF CHUNK_06 RESULTS AVAILABLE
# ============================================================================

if __name__ == '__main__' or 'chunk06_results' in globals():
    try:
        if 'chunk06_results' in globals():
            print("[OK] Found CHUNK_06 results\n")
            chunk07_results = run_chunk07(chunk06_results=chunk06_results)
            print("✓ Results stored in 'chunk07_results'")
            print("✓ Ready for CHUNK_08 - Explainability & Feature Analysis\n")
        else:
            print("[INFO] CHUNK_06 results not found. Call manually:")
            print("    chunk07_results = run_chunk07(chunk06_results=chunk06_results)")
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        print("\n[INFO] To run manually, use:")
        print("    chunk07_results = run_chunk07(chunk06_results=chunk06_results)")
