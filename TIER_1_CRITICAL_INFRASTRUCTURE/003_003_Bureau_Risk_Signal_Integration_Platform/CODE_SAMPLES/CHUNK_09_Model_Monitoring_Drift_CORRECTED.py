"""
PROBLEM 20: BUREAU RISK SIGNAL INTEGRATION
CHUNK 09: MODEL MONITORING & DRIFT DETECTION (CORRECTED PATHS)

Purpose:
  Setup production monitoring framework
  Track model performance over time
  Detect data drift (feature distribution changes)
  Detect prediction drift (output distribution changes)
  Detect performance drift (metric degradation)
  Monitor feature drift using statistical tests
  Generate monitoring alerts & recommendations
  Create monitoring dashboard visualizations
  Register outputs for CHUNK_13 aggregation

Compliance: BCBS 239, SOX 404, JP Morgan, Goldman Sachs
Methodology: Statistical Drift Detection, Performance Monitoring

Author: Enterprise AI System
Date: August 12, 2026
Version: 1.0.0-PRODUCTION
"""

import pandas as pd
import numpy as np
import json
import os
import logging
import pickle
import warnings
from datetime import datetime
from scipy import stats
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - CHUNK_09 - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# CORRECTED PATH SETUP
# ============================================================================
try:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    IS_JUPYTER = False
except NameError:
    IS_JUPYTER = True
    BASE_PATH = os.getcwd()

PROBLEM_20_ROOT = r"C:\Users\rnand\Documents\home-credit-default-risk\Enterprise_AI_Workflows\020_Bureau_Risk_Signal_Integration"
ROOT_PATH = PROBLEM_20_ROOT

CHUNK_04_PATH = os.path.join(ROOT_PATH, "04_Feature_Engineering", "Engineered_Data")
CHUNK_05_MODELS = os.path.join(ROOT_PATH, "05_Model_Development", "Trained_Models")
CHUNK_09_LOGS = os.path.join(ROOT_PATH, "09_Model_Monitoring", "Monitoring_Logs")
CHUNK_09_REPORTS = os.path.join(ROOT_PATH, "09_Model_Monitoring", "Reports")
CHUNK_09_CHARTS = os.path.join(ROOT_PATH, "09_Model_Monitoring", "Charts")
CHUNK_09_GOVERNANCE = os.path.join(ROOT_PATH, "09_Model_Monitoring", "Governance")
REGISTRY_PATH = os.path.join(ROOT_PATH, "00_Report_Registry")

for path in [CHUNK_09_LOGS, CHUNK_09_REPORTS, CHUNK_09_CHARTS, CHUNK_09_GOVERNANCE, REGISTRY_PATH]:
    os.makedirs(path, exist_ok=True)

logger.info(f"Problem 20 Root: {ROOT_PATH}")

# ============================================================================
# STEP 1: LOAD DATA & MODEL
# ============================================================================
logger.info("\n" + "╔" + "=" * 68 + "╗")
logger.info("║" + " CHUNK 09: MODEL MONITORING & DRIFT DETECTION ".center(68) + "║")
logger.info("╚" + "=" * 68 + "╝\n")

logger.info("=" * 70)
logger.info("STEP 1: LOADING DATA & MODEL")
logger.info("=" * 70)

# Load data
csv_path = os.path.join(CHUNK_04_PATH, 'bureau_risk_engineered.csv')
df = pd.read_csv(csv_path)
X = df.drop('TARGET', axis=1) if 'TARGET' in df.columns else df
y = df['TARGET'] if 'TARGET' in df.columns else None

logger.info(f"✓ Loaded data: {df.shape[0]:,} rows × {df.shape[1]} columns")

# Load model
model_path = os.path.join(CHUNK_05_MODELS, 'random_forest_v1.pkl')
with open(model_path, 'rb') as f:
    best_model = pickle.load(f)
logger.info(f"✓ Loaded model: Random Forest")

# ============================================================================
# STEP 2: ESTABLISH BASELINE PERFORMANCE
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 2: ESTABLISHING BASELINE PERFORMANCE METRICS")
logger.info("=" * 70)

# Split data into baseline (80%) and monitoring (20%)
baseline_size = int(0.8 * len(X))
X_baseline = X.iloc[:baseline_size]
y_baseline = y.iloc[:baseline_size]
X_monitoring = X.iloc[baseline_size:]
y_monitoring = y.iloc[baseline_size:]

# Get predictions
y_pred_baseline = best_model.predict_proba(X_baseline)[:, 1]
y_pred_monitoring = best_model.predict_proba(X_monitoring)[:, 1]

# Calculate baseline metrics
baseline_metrics = {
    'auc': float(roc_auc_score(y_baseline, y_pred_baseline)),
    'f1': float(f1_score(y_baseline, (y_pred_baseline >= 0.5).astype(int))),
    'precision': float(precision_score(y_baseline, (y_pred_baseline >= 0.5).astype(int))),
    'recall': float(recall_score(y_baseline, (y_pred_baseline >= 0.5).astype(int))),
    'accuracy': float(accuracy_score(y_baseline, (y_pred_baseline >= 0.5).astype(int)))
}

logger.info(f"✓ Baseline metrics established:")
logger.info(f"  ├─ AUC: {baseline_metrics['auc']:.4f}")
logger.info(f"  ├─ F1: {baseline_metrics['f1']:.4f}")
logger.info(f"  ├─ Precision: {baseline_metrics['precision']:.4f}")
logger.info(f"  └─ Recall: {baseline_metrics['recall']:.4f}")

# ============================================================================
# STEP 3: MONITOR PERFORMANCE
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 3: MONITORING CURRENT PERFORMANCE")
logger.info("=" * 70)

monitoring_metrics = {
    'auc': float(roc_auc_score(y_monitoring, y_pred_monitoring)),
    'f1': float(f1_score(y_monitoring, (y_pred_monitoring >= 0.5).astype(int))),
    'precision': float(precision_score(y_monitoring, (y_pred_monitoring >= 0.5).astype(int))),
    'recall': float(recall_score(y_monitoring, (y_pred_monitoring >= 0.5).astype(int))),
    'accuracy': float(accuracy_score(y_monitoring, (y_pred_monitoring >= 0.5).astype(int)))
}

logger.info(f"✓ Current monitoring metrics:")
logger.info(f"  ├─ AUC: {monitoring_metrics['auc']:.4f}")
logger.info(f"  ├─ F1: {monitoring_metrics['f1']:.4f}")
logger.info(f"  ├─ Precision: {monitoring_metrics['precision']:.4f}")
logger.info(f"  └─ Recall: {monitoring_metrics['recall']:.4f}")

# Calculate metric changes
metric_changes = {
    'auc_change': float(monitoring_metrics['auc'] - baseline_metrics['auc']),
    'f1_change': float(monitoring_metrics['f1'] - baseline_metrics['f1']),
    'precision_change': float(monitoring_metrics['precision'] - baseline_metrics['precision']),
    'recall_change': float(monitoring_metrics['recall'] - baseline_metrics['recall'])
}

logger.info(f"\n✓ Performance changes from baseline:")
for metric, change in metric_changes.items():
    direction = "📈" if change > 0 else "📉" if change < 0 else "➡️"
    logger.info(f"  {direction} {metric}: {change:+.4f}")

# ============================================================================
# STEP 4: DATA DRIFT DETECTION
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 4: DATA DRIFT DETECTION (KOLMOGOROV-SMIRNOV TEST)")
logger.info("=" * 70)

data_drift_results = {}

for col in X.select_dtypes(include=[np.number]).columns[:20]:  # Top 20 numeric features
    baseline_dist = X_baseline[col].dropna()
    monitoring_dist = X_monitoring[col].dropna()

    # Kolmogorov-Smirnov test
    ks_stat, p_value = stats.ks_2samp(baseline_dist, monitoring_dist)

    # Drift detected if p-value < 0.05
    drift_detected = p_value < 0.05

    data_drift_results[col] = {
        'ks_statistic': float(ks_stat),
        'p_value': float(p_value),
        'drift_detected': bool(drift_detected),
        'baseline_mean': float(baseline_dist.mean()),
        'monitoring_mean': float(monitoring_dist.mean()),
        'mean_shift_percent': float(100 * abs(monitoring_dist.mean() - baseline_dist.mean()) / (abs(baseline_dist.mean()) + 1e-8))
    }

features_with_drift = [f for f, r in data_drift_results.items() if r['drift_detected']]

logger.info(f"✓ Data drift analysis completed:")
logger.info(f"  ├─ Features analyzed: {len(data_drift_results)}")
logger.info(f"  ├─ Features with drift: {len(features_with_drift)}")
if features_with_drift:
    logger.info(f"  └─ Drifted features: {', '.join(features_with_drift[:5])}")
else:
    logger.info(f"  └─ No significant drift detected ✓")

# ============================================================================
# STEP 5: PREDICTION DRIFT DETECTION
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 5: PREDICTION DRIFT DETECTION")
logger.info("=" * 70)

# Compare prediction distributions
baseline_pred_mean = y_pred_baseline.mean()
monitoring_pred_mean = y_pred_monitoring.mean()
pred_dist_shift = abs(monitoring_pred_mean - baseline_pred_mean)

# Kolmogorov-Smirnov test on predictions
ks_stat_pred, p_value_pred = stats.ks_2samp(y_pred_baseline, y_pred_monitoring)

prediction_drift = {
    'baseline_prediction_mean': float(baseline_pred_mean),
    'monitoring_prediction_mean': float(monitoring_pred_mean),
    'prediction_shift': float(pred_dist_shift),
    'ks_statistic': float(ks_stat_pred),
    'p_value': float(p_value_pred),
    'drift_detected': bool(p_value_pred < 0.05)
}

logger.info(f"✓ Prediction drift analysis:")
logger.info(f"  ├─ Baseline mean prediction: {baseline_pred_mean:.4f}")
logger.info(f"  ├─ Monitoring mean prediction: {monitoring_pred_mean:.4f}")
logger.info(f"  ├─ Prediction shift: {pred_dist_shift:.4f}")
logger.info(f"  └─ Drift status: {'⚠️ DETECTED' if prediction_drift['drift_detected'] else '✓ No drift'}")

# ============================================================================
# STEP 6: PERFORMANCE DRIFT DETECTION
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 6: PERFORMANCE DRIFT DETECTION")
logger.info("=" * 70)

# Set alert thresholds (5% degradation)
auc_threshold = 0.05
performance_alerts = {}

for metric, baseline_val in baseline_metrics.items():
    monitoring_val = monitoring_metrics[metric]
    degradation = baseline_val - monitoring_val
    degradation_percent = 100 * degradation / (baseline_val + 1e-8)

    alert_triggered = degradation_percent > auc_threshold

    performance_alerts[metric] = {
        'baseline': baseline_val,
        'current': monitoring_val,
        'degradation': float(degradation),
        'degradation_percent': float(degradation_percent),
        'alert_triggered': alert_triggered,
        'recommendation': 'RETRAIN MODEL' if alert_triggered else 'Monitor normally'
    }

logger.info(f"✓ Performance drift analysis:")
for metric, alert in performance_alerts.items():
    status = "🚨 ALERT" if alert['alert_triggered'] else "✓ OK"
    logger.info(f"  {status} {metric}: {alert['degradation_percent']:+.2f}%")

# ============================================================================
# STEP 7: MONITORING DASHBOARD & ALERTS
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 7: GENERATING MONITORING DASHBOARD & ALERTS")
logger.info("=" * 70)

monitoring_dashboard = {
    'timestamp': datetime.now().isoformat(),
    'baseline_period': {
        'records': len(X_baseline),
        'metrics': baseline_metrics
    },
    'monitoring_period': {
        'records': len(X_monitoring),
        'metrics': monitoring_metrics,
        'metric_changes': metric_changes
    },
    'data_drift': data_drift_results,
    'prediction_drift': prediction_drift,
    'performance_drift': performance_alerts,
    'alerts': {
        'critical': len([a for a in performance_alerts.values() if a['alert_triggered']]),
        'data_drift_features': len(features_with_drift),
        'prediction_drift_detected': prediction_drift['drift_detected'],
        'overall_status': 'ALERT' if any(a['alert_triggered'] for a in performance_alerts.values()) else 'HEALTHY'
    },
    'recommendations': [
        f"Monitor {len(features_with_drift)} features with data drift" if features_with_drift else "No data drift detected",
        f"Retraining required - {sum(1 for a in performance_alerts.values() if a['alert_triggered'])} metrics degraded" if any(a['alert_triggered'] for a in performance_alerts.values()) else "Model performance stable",
        "Check prediction distribution for shifts" if prediction_drift['drift_detected'] else "Prediction distribution stable",
        "Increase monitoring frequency for high-drift features"
    ]
}

logger.info(f"✓ Monitoring dashboard generated")
logger.info(f"  ├─ Overall status: {monitoring_dashboard['alerts']['overall_status']}")
logger.info(f"  ├─ Critical alerts: {monitoring_dashboard['alerts']['critical']}")
logger.info(f"  └─ Data drift features: {monitoring_dashboard['alerts']['data_drift_features']}")

# Save dashboard
dashboard_path = os.path.join(CHUNK_09_REPORTS, 'monitoring_dashboard.json')
with open(dashboard_path, 'w') as f:
    json.dump(monitoring_dashboard, f, indent=2, default=str)

# ============================================================================
# STEP 8: GENERATE MONITORING VISUALIZATIONS
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 8: GENERATING MONITORING VISUALIZATIONS")
logger.info("=" * 70)

# 1. Performance metrics comparison
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle('Model Performance Monitoring: Baseline vs Current', fontsize=14, fontweight='bold')

metrics_to_plot = ['auc', 'f1', 'precision', 'recall', 'accuracy']
colors = ['green' if monitoring_metrics[m] >= baseline_metrics[m] else 'red' for m in metrics_to_plot]

for idx, metric in enumerate(metrics_to_plot):
    row, col = idx // 3, idx % 3
    x_pos = [0, 1]
    values = [baseline_metrics[metric], monitoring_metrics[metric]]
    bars = axes[row, col].bar(x_pos, values, color=['blue', colors[idx]])
    axes[row, col].set_ylabel('Score')
    axes[row, col].set_title(metric.upper())
    axes[row, col].set_ylim([0, 1])
    axes[row, col].set_xticks(x_pos)
    axes[row, col].set_xticklabels(['Baseline', 'Current'])

    # Add value labels
    for i, v in enumerate(values):
        axes[row, col].text(i, v + 0.02, f'{v:.3f}', ha='center')

# Remove extra subplot
axes[1, 2].remove()

plt.tight_layout()
perf_chart_path = os.path.join(CHUNK_09_CHARTS, 'performance_monitoring.png')
plt.savefig(perf_chart_path, dpi=100, bbox_inches='tight')
plt.close()
logger.info(f"✓ Saved: performance_monitoring.png")

# 2. Prediction distribution comparison
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].hist(y_pred_baseline, bins=30, alpha=0.7, label='Baseline', color='blue')
axes[0].hist(y_pred_monitoring, bins=30, alpha=0.7, label='Current', color='orange')
axes[0].set_xlabel('Predicted Probability')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Prediction Distribution Comparison')
axes[0].legend()

# Alert status
alert_colors = ['red' if a['alert_triggered'] else 'green' for a in performance_alerts.values()]
axes[1].barh(list(performance_alerts.keys()), [a['degradation_percent'] for a in performance_alerts.values()], color=alert_colors)
axes[1].axvline(x=5, color='red', linestyle='--', label='Alert threshold')
axes[1].set_xlabel('Performance Degradation (%)')
axes[1].set_title('Performance Degradation by Metric')
axes[1].legend()

plt.tight_layout()
drift_chart_path = os.path.join(CHUNK_09_CHARTS, 'drift_detection.png')
plt.savefig(drift_chart_path, dpi=100, bbox_inches='tight')
plt.close()
logger.info(f"✓ Saved: drift_detection.png")

# ============================================================================
# STEP 9: REGISTER WITH REPORTING FRAMEWORK
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 9: REGISTERING WITH REPORTING FRAMEWORK")
logger.info("=" * 70)

chunk_registry = {
    'chunk_id': 'CHUNK_09',
    'chunk_name': 'Model Monitoring & Drift Detection',
    'execution_timestamp': datetime.now().isoformat(),
    'status': 'COMPLETED',
    'description': 'Production monitoring framework with drift detection',
    'monitoring_summary': {
        'baseline_records': len(X_baseline),
        'monitoring_records': len(X_monitoring),
        'overall_status': monitoring_dashboard['alerts']['overall_status']
    },
    'baseline_metrics': baseline_metrics,
    'current_metrics': monitoring_metrics,
    'metric_changes': metric_changes,
    'alerts': monitoring_dashboard['alerts'],
    'data_drift_detected_features': features_with_drift[:10],
    'prediction_drift': prediction_drift,
    'performance_alerts': performance_alerts,
    'outputs': [
        {'type': 'json', 'path': dashboard_path, 'description': 'Comprehensive monitoring dashboard'},
        {'type': 'png', 'path': perf_chart_path, 'description': 'Performance metrics comparison'},
        {'type': 'png', 'path': drift_chart_path, 'description': 'Drift detection visualization'}
    ],
    'monitoring_thresholds': {
        'data_drift_pvalue': 0.05,
        'performance_degradation_percent': 5.0
    },
    'recommendations': monitoring_dashboard['recommendations'],
    'ready_for_next_chunk': True,
    'next_chunk': 'CHUNK_10 (Production Deployment)'
}

registry_file = os.path.join(REGISTRY_PATH, 'chunk_09_report.json')
with open(registry_file, 'w') as f:
    json.dump(chunk_registry, f, indent=2, default=str)
logger.info(f"✓ Registered: {registry_file}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("CHUNK 09 SUMMARY - MODEL MONITORING & DRIFT DETECTION")
logger.info("=" * 70)
logger.info(f"✓ Baseline metrics established (80% data)")
logger.info(f"✓ Current monitoring metrics calculated (20% data)")
logger.info(f"✓ Data drift detection: {len(features_with_drift)} features with drift")
logger.info(f"✓ Prediction drift detection: {'⚠️ DETECTED' if prediction_drift['drift_detected'] else '✓ Stable'}")
logger.info(f"✓ Performance drift: {sum(1 for a in performance_alerts.values() if a['alert_triggered'])} alerts triggered")
logger.info(f"✓ Visualizations: 2 monitoring charts generated")
logger.info(f"✓ Overall status: {monitoring_dashboard['alerts']['overall_status']}")
logger.info(f"✓ Status: READY FOR CHUNK_10")
logger.info("=" * 70)
logger.info("\n✅ CHUNK 09 COMPLETED SUCCESSFULLY\n")
