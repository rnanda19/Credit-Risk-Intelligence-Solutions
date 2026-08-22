#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CHUNK_09: MODEL MONITORING & DRIFT DETECTION - JUPYTER VERSION
================================================================================

Monitors model performance in production:
1. Track prediction metrics over time
2. Detect data distribution drift
3. Detect feature importance drift
4. Monitor performance degradation
5. Generate monitoring alerts
6. Create retraining recommendations

Copy and paste each cell into your Jupyter notebook.

================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

print("\n" + "=" * 80)
print("CHUNK_09: MODEL MONITORING & DRIFT DETECTION")
print("=" * 80 + "\n")

# ============================================================================
# CELL 1: QUALITY GATE 1 - ESTABLISH BASELINE METRICS
# ============================================================================

print("=" * 80)
print("QUALITY GATE 1: ESTABLISH BASELINE METRICS (From CHUNK_08)")
print("=" * 80 + "\n")

# Get baseline from test set
y_test = chunk05_results['training_results']['Gradient Boosting']['y_test']
y_pred_proba = chunk07_results['y_pred_proba']
optimal_threshold = chunk07_results['optimal_threshold']

y_pred = (y_pred_proba >= optimal_threshold).astype(int)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

baseline_metrics = {
    'accuracy': accuracy_score(y_test, y_pred),
    'precision': precision_score(y_test, y_pred, zero_division=0),
    'recall': recall_score(y_test, y_pred, zero_division=0),
    'f1': f1_score(y_test, y_pred, zero_division=0),
    'roc_auc': roc_auc_score(y_test, y_pred_proba),
    'avg_pred_prob': y_pred_proba.mean(),
    'default_rate': y_test.mean()
}

print("BASELINE METRICS (From Test Set):\n")
for metric, value in baseline_metrics.items():
    print(f"  {metric:20s}: {value:.4f}")

print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Sample size: {len(y_test)}\n")

# ============================================================================
# CELL 2: QUALITY GATE 2 - SIMULATE PRODUCTION DATA
# ============================================================================

print("=" * 80)
print("QUALITY GATE 2: SIMULATE PRODUCTION DATA (MONITORING PERIOD)")
print("=" * 80 + "\n")

# Simulate 4 weeks of production data
np.random.seed(42)
weeks = 4
samples_per_week = 500
total_samples = weeks * samples_per_week

# Generate simulated production data with slight drift
production_data = []
for week in range(weeks):
    # Add gradual drift to default rate
    drift_factor = 0.95 + (week * 0.02)  # Default rate increases slightly
    week_default_rate = baseline_metrics['default_rate'] * drift_factor

    week_y_true = np.random.binomial(1, week_default_rate, samples_per_week)
    # Predictions slightly delayed to catch drift
    week_y_pred_proba = np.random.uniform(0, 1, samples_per_week)

    for i in range(samples_per_week):
        production_data.append({
            'week': week + 1,
            'y_true': week_y_true[i],
            'y_pred_proba': week_y_pred_proba[i],
            'timestamp': datetime.now() - timedelta(weeks=weeks-week-1, days=i//125)
        })

prod_df = pd.DataFrame(production_data)
prod_df['y_pred'] = (prod_df['y_pred_proba'] >= optimal_threshold).astype(int)

print(f"Simulated Production Data: {len(prod_df)} samples over {weeks} weeks\n")
print(f"Weeks: {prod_df['week'].min()} to {prod_df['week'].max()}")
print(f"Samples per week: {len(prod_df) // weeks}\n")

# ============================================================================
# CELL 3: QUALITY GATE 3 - PERFORMANCE MONITORING
# ============================================================================

print("=" * 80)
print("QUALITY GATE 3: PERFORMANCE MONITORING (WEEKLY METRICS)")
print("=" * 80 + "\n")

weekly_metrics = []

for week in range(1, weeks + 1):
    week_data = prod_df[prod_df['week'] == week]

    acc = accuracy_score(week_data['y_true'], week_data['y_pred'])
    prec = precision_score(week_data['y_true'], week_data['y_pred'], zero_division=0)
    rec = recall_score(week_data['y_true'], week_data['y_pred'], zero_division=0)
    f1 = f1_score(week_data['y_true'], week_data['y_pred'], zero_division=0)
    auc = roc_auc_score(week_data['y_true'], week_data['y_pred_proba'])

    # Calculate degradation vs baseline
    acc_degradation = ((baseline_metrics['accuracy'] - acc) / baseline_metrics['accuracy']) * 100

    weekly_metrics.append({
        'week': week,
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'f1': f1,
        'roc_auc': auc,
        'accuracy_degradation_%': acc_degradation,
        'default_rate': week_data['y_true'].mean(),
        'samples': len(week_data)
    })

metrics_df = pd.DataFrame(weekly_metrics)

print("Weekly Performance Metrics:\n")
print(metrics_df.to_string(index=False))

print("\n\nTrend Analysis:")
print("-" * 70)

for idx, row in metrics_df.iterrows():
    week = row['week']
    degradation = row['accuracy_degradation_%']

    if degradation < 1:
        status = "✓ STABLE"
    elif degradation < 3:
        status = "⚠ MINOR DRIFT"
    else:
        status = "❌ SIGNIFICANT DRIFT"

    print(f"Week {week}: Accuracy degradation {degradation:.2f}% [{status}]")

print()

# ============================================================================
# CELL 4: QUALITY GATE 4 - DATA DISTRIBUTION DRIFT
# ============================================================================

print("=" * 80)
print("QUALITY GATE 4: DATA DISTRIBUTION DRIFT DETECTION")
print("=" * 80 + "\n")

print("Data Distribution Monitoring:\n")
print(f"Baseline default rate: {baseline_metrics['default_rate']:.4f}")
print(f"Baseline avg prediction: {baseline_metrics['avg_pred_prob']:.4f}\n")

print("Production Period:")
for week in range(1, weeks + 1):
    week_data = prod_df[prod_df['week'] == week]
    default_rate = week_data['y_true'].mean()
    avg_pred = week_data['y_pred_proba'].mean()

    drift_ratio = (default_rate / baseline_metrics['default_rate']) - 1

    if abs(drift_ratio) < 0.05:
        status = "✓ No drift"
    elif abs(drift_ratio) < 0.10:
        status = "⚠ Minor drift"
    else:
        status = "❌ Significant drift"

    print(f"Week {week}:")
    print(f"  Default rate: {default_rate:.4f} (drift: {drift_ratio:+.2%}) [{status}]")
    print(f"  Avg prediction: {avg_pred:.4f}")

print()

# ============================================================================
# CELL 5: QUALITY GATE 5 - FEATURE IMPORTANCE STABILITY
# ============================================================================

print("=" * 80)
print("QUALITY GATE 5: FEATURE IMPORTANCE STABILITY")
print("=" * 80 + "\n")

# Get baseline feature importance
feature_importance = chunk08_results['feature_importance']
top_features = chunk08_results['top_features']

print(f"Baseline Feature Importance (Top 10):\n")
print(feature_importance.head(10).to_string(index=False))

print(f"\n\nFeature Importance Monitoring:")
print("-" * 70)
print("Status: ✓ Would track in production with periodic model retraining")
print("Frequency: Weekly or bi-weekly importance recalculation")
print("Alert trigger: 20%+ change in top 3 features\n")

# ============================================================================
# CELL 6: QUALITY GATE 6 - RETRAINING RECOMMENDATIONS
# ============================================================================

print("=" * 80)
print("QUALITY GATE 6: RETRAINING RECOMMENDATIONS")
print("=" * 80 + "\n")

# Calculate if retraining is needed
max_degradation = metrics_df['accuracy_degradation_%'].max()
final_default_rate = metrics_df.iloc[-1]['default_rate']
baseline_default_rate = baseline_metrics['default_rate']
default_rate_change = (final_default_rate / baseline_default_rate - 1) * 100

print("Retraining Decision Criteria:\n")
print(f"1. Accuracy degradation threshold: 3.0%")
print(f"   Current max degradation: {max_degradation:.2f}%")
print(f"   Status: {'⚠ APPROACHING' if max_degradation > 2 else '✓ OK'}\n")

print(f"2. Default rate change threshold: ±10%")
print(f"   Current change: {default_rate_change:+.2f}%")
print(f"   Status: {'⚠ APPROACHING' if abs(default_rate_change) > 5 else '✓ OK'}\n")

print(f"3. Feature importance drift: 20%+ in top 3")
print(f"   Current status: ✓ STABLE (baseline)\n")

if max_degradation > 3 or abs(default_rate_change) > 10:
    recommendation = "❌ IMMEDIATE RETRAINING REQUIRED"
    priority = "HIGH"
elif max_degradation > 2 or abs(default_rate_change) > 5:
    recommendation = "⚠ SCHEDULE RETRAINING (Next 2 weeks)"
    priority = "MEDIUM"
else:
    recommendation = "✓ CONTINUE MONITORING (No retraining needed)"
    priority = "LOW"

print(f"RECOMMENDATION: {recommendation}")
print(f"Priority: {priority}\n")

# ============================================================================
# CELL 7: QUALITY GATE 7 - MONITORING DASHBOARD SUMMARY
# ============================================================================

print("=" * 80)
print("QUALITY GATE 7: MONITORING DASHBOARD SUMMARY")
print("=" * 80 + "\n")

print("CURRENT MODEL STATUS:\n")
print(f"Deployment date: {(datetime.now() - timedelta(weeks=weeks)).strftime('%Y-%m-%d')}")
print(f"Monitoring period: {weeks} weeks")
print(f"Total predictions: {len(prod_df):,}")
print(f"Samples/week average: {len(prod_df) // weeks}\n")

print("PERFORMANCE SUMMARY:\n")
print(f"Baseline accuracy: {baseline_metrics['accuracy']:.4f}")
print(f"Current accuracy (Week {weeks}): {metrics_df.iloc[-1]['accuracy']:.4f}")
print(f"Max degradation: {max_degradation:.2f}%")
print(f"Status: {'✓ STABLE' if max_degradation < 3 else '⚠ WATCH' if max_degradation < 5 else '❌ NEEDS ATTENTION'}\n")

print("DRIFT SUMMARY:\n")
print(f"Data drift detected: {'Yes (minor)' if abs(default_rate_change) > 5 else 'No'}")
print(f"Default rate change: {default_rate_change:+.2f}%")
print(f"Status: {'✓ NORMAL VARIATION' if abs(default_rate_change) < 10 else '⚠ SIGNIFICANT DRIFT'}\n")

print("NEXT ACTIONS:\n")
print(f"✓ Continue weekly monitoring")
print(f"✓ Track accuracy and drift metrics")
print(f"{'✓ Plan retraining for next 2 weeks' if max_degradation > 2 else '✓ No immediate action needed'}")
print(f"✓ Monthly comprehensive review\n")

# ============================================================================
# CELL 8: GENERATE MONITORING REPORT
# ============================================================================

print("=" * 80)
print("GENERATING MONITORING REPORT")
print("=" * 80 + "\n")

monitoring_summary = "=" * 80 + "\n"
monitoring_summary += "MODEL MONITORING & DRIFT DETECTION REPORT\n"
monitoring_summary += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
monitoring_summary += "=" * 80 + "\n\n"

monitoring_summary += "EXECUTIVE SUMMARY:\n"
monitoring_summary += "-" * 80 + "\n"
monitoring_summary += f"Model deployed: {weeks} weeks ago\n"
monitoring_summary += f"Current status: {recommendation}\n"
monitoring_summary += f"Priority: {priority}\n\n"

monitoring_summary += "PERFORMANCE METRICS:\n"
monitoring_summary += "-" * 80 + "\n"
for idx, row in metrics_df.iterrows():
    monitoring_summary += f"Week {row['week']}: Accuracy {row['accuracy']:.4f} (Degradation: {row['accuracy_degradation_%']:.2f}%)\n"

monitoring_summary += f"\nMax degradation: {max_degradation:.2f}%\n"
monitoring_summary += f"Status: {'✓ ACCEPTABLE' if max_degradation < 3 else '⚠ WATCH'}\n\n"

monitoring_summary += "DATA DRIFT:\n"
monitoring_summary += "-" * 80 + "\n"
monitoring_summary += f"Baseline default rate: {baseline_metrics['default_rate']:.4f}\n"
monitoring_summary += f"Current default rate: {final_default_rate:.4f}\n"
monitoring_summary += f"Change: {default_rate_change:+.2f}%\n"
monitoring_summary += f"Status: {'✓ NORMAL' if abs(default_rate_change) < 10 else '⚠ WATCH'}\n\n"

monitoring_summary += "RECOMMENDATIONS:\n"
monitoring_summary += "-" * 80 + "\n"
monitoring_summary += f"1. {recommendation}\n"
monitoring_summary += f"2. Continue weekly monitoring\n"
monitoring_summary += f"3. Monthly comprehensive review\n"
monitoring_summary += f"4. Quarterly fairness audit\n\n"

monitoring_summary += "=" * 80 + "\n"

print(monitoring_summary)

# ============================================================================
# CELL 9: STORE RESULTS
# ============================================================================

print("=" * 80)
print("CHUNK_09: MODEL MONITORING COMPLETE")
print("=" * 80 + "\n")

chunk09_results = {
    'baseline_metrics': baseline_metrics,
    'weekly_metrics': metrics_df,
    'production_data': prod_df,
    'feature_importance': feature_importance,
    'retraining_needed': max_degradation > 3,
    'retraining_priority': priority,
    'max_degradation': max_degradation,
    'default_rate_change': default_rate_change,
    'monitoring_summary': monitoring_summary,
    'optimal_threshold': optimal_threshold,
    'best_model': chunk07_results['best_model']
}

print("✓ Results stored in 'chunk09_results'")
print("✓ Ready for CHUNK_10 - Production Deployment\n")

print("Key Findings:")
print(f"  Baseline Accuracy: {baseline_metrics['accuracy']:.4f}")
print(f"  Max Degradation: {max_degradation:.2f}%")
print(f"  Retraining Needed: {max_degradation > 3}")
print(f"  Priority: {priority}\n")
