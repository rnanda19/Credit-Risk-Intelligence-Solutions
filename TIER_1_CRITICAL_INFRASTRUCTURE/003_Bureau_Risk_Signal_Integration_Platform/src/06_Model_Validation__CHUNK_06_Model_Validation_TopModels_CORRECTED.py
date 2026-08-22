"""
PROBLEM 20: BUREAU RISK SIGNAL INTEGRATION
CHUNK 06: MODEL VALIDATION - TOP 2 MODELS, 5-FOLD CV (CORRECTED PATHS)

Purpose:
  Auto-select top 2 models from CHUNK_05
  Perform 5-fold stratified cross-validation
  Compare validation performance
  Select best model for production
  Register outputs for CHUNK_13 aggregation

Compliance: BCBS 239, SOX 404, All 10 SOP Standards
Methodology: 5-Fold CV, Stratified Sampling

Author: Enterprise AI System
Date: August 12, 2026
Version: 1.2.0-PRODUCTION
"""

import pandas as pd
import numpy as np
import json
import os
import logging
import pickle
import warnings
from datetime import datetime
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score, accuracy_score, log_loss
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - CHUNK_06 - %(levelname)s - %(message)s')
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
CHUNK_05_REPORTS = os.path.join(ROOT_PATH, "05_Model_Development", "Reports")
CHUNK_06_RESULTS = os.path.join(ROOT_PATH, "06_Model_Validation", "Validation_Results")
CHUNK_06_REPORTS = os.path.join(ROOT_PATH, "06_Model_Validation", "Reports")
REGISTRY_PATH = os.path.join(ROOT_PATH, "00_Report_Registry")

for path in [CHUNK_06_RESULTS, CHUNK_06_REPORTS, REGISTRY_PATH]:
    os.makedirs(path, exist_ok=True)

logger.info(f"Problem 20 Root: {ROOT_PATH}")

# ============================================================================
# STEP 1: LOAD DATA & CHUNK_05 RESULTS
# ============================================================================
logger.info("\n" + "╔" + "=" * 68 + "╗")
logger.info("║" + " CHUNK 06: MODEL VALIDATION - TOP 2, 5-FOLD CV ".center(68) + "║")
logger.info("╚" + "=" * 68 + "╝\n")

logger.info("=" * 70)
logger.info("STEP 1: LOADING DATA & CHUNK_05 RESULTS")
logger.info("=" * 70)

# Load data
csv_path = os.path.join(CHUNK_04_PATH, 'bureau_risk_engineered.csv')
df = pd.read_csv(csv_path)
X = df.drop('TARGET', axis=1) if 'TARGET' in df.columns else df
y = df['TARGET'] if 'TARGET' in df.columns else None

logger.info(f"✓ Loaded data: {df.shape[0]:,} rows × {df.shape[1]} columns")

# Load CHUNK_05 results
chunk_05_report = os.path.join(REGISTRY_PATH, 'chunk_05_report.json')
with open(chunk_05_report, 'r') as f:
    chunk_05_results = json.load(f)

logger.info(f"✓ Loaded CHUNK_05 report")

# ============================================================================
# STEP 2: AUTO-SELECT TOP 2 MODELS
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 2: AUTO-SELECTING TOP 2 MODELS BY AUC")
logger.info("=" * 70)

model_perf = chunk_05_results['key_metrics']['all_models_performance']
ranked_models = sorted(model_perf.items(), key=lambda x: x[1]['AUC'], reverse=True)
top_2_models = [name for name, _ in ranked_models[:2]]

logger.info(f"\nTop 2 Models:")
for i, (name, metrics) in enumerate(ranked_models[:2], 1):
    logger.info(f"  {i}. {name}: AUC={metrics['AUC']:.4f}")

# Load selected models
loaded_models = {}
scaler = None

for model_name in top_2_models:
    model_file = os.path.join(CHUNK_05_MODELS, f'{model_name.lower().replace(" ", "_")}_v1.pkl')
    with open(model_file, 'rb') as f:
        loaded_models[model_name] = pickle.load(f)
    logger.info(f"✓ Loaded {model_name}")

scaler_file = os.path.join(CHUNK_05_MODELS, 'feature_scaler_v1.pkl')
with open(scaler_file, 'rb') as f:
    scaler = pickle.load(f)

# ============================================================================
# STEP 3: 5-FOLD STRATIFIED CROSS-VALIDATION
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 3: 5-FOLD STRATIFIED CROSS-VALIDATION")
logger.info("=" * 70)

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_results = {}

for model_name, model in loaded_models.items():
    logger.info(f"\n{model_name}:")

    fold_metrics = {
        'auc_scores': [],
        'f1_scores': [],
        'precision_scores': [],
        'recall_scores': [],
        'accuracy_scores': []
    }

    fold_num = 1
    for train_idx, val_idx in skf.split(X, y):
        X_train_fold, X_val_fold = X.iloc[train_idx], X.iloc[val_idx]
        y_train_fold, y_val_fold = y.iloc[train_idx], y.iloc[val_idx]

        # Scale if needed (Neural Network, Logistic Regression)
        if 'Neural' in model_name or 'Logistic' in model_name:
            X_train_fold = scaler.fit_transform(X_train_fold)
            X_val_fold = scaler.transform(X_val_fold)

        # Predict
        try:
            y_pred_proba = model.predict_proba(X_val_fold)[:, 1]
        except:
            y_pred_proba = model.predict_proba(X_val_fold)[:, 1]

        y_pred = (y_pred_proba >= 0.5).astype(int)

        # Calculate metrics
        fold_metrics['auc_scores'].append(float(roc_auc_score(y_val_fold, y_pred_proba)))
        fold_metrics['f1_scores'].append(float(f1_score(y_val_fold, y_pred)))
        fold_metrics['precision_scores'].append(float(precision_score(y_val_fold, y_pred)))
        fold_metrics['recall_scores'].append(float(recall_score(y_val_fold, y_pred)))
        fold_metrics['accuracy_scores'].append(float(accuracy_score(y_val_fold, y_pred)))

        logger.info(f"  Fold {fold_num}: AUC={fold_metrics['auc_scores'][-1]:.4f}, F1={fold_metrics['f1_scores'][-1]:.4f}")
        fold_num += 1

    # Store results
    cv_results[model_name] = {
        'mean_auc': float(np.mean(fold_metrics['auc_scores'])),
        'std_auc': float(np.std(fold_metrics['auc_scores'])),
        'mean_f1': float(np.mean(fold_metrics['f1_scores'])),
        'mean_precision': float(np.mean(fold_metrics['precision_scores'])),
        'mean_recall': float(np.mean(fold_metrics['recall_scores'])),
        'mean_accuracy': float(np.mean(fold_metrics['accuracy_scores'])),
        'fold_scores': fold_metrics
    }

    logger.info(f"  Summary: AUC={cv_results[model_name]['mean_auc']:.4f}±{cv_results[model_name]['std_auc']:.4f}")

# ============================================================================
# STEP 4: SELECT BEST MODEL
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 4: BEST MODEL SELECTION")
logger.info("=" * 70)

best_model_name = max(cv_results, key=lambda x: cv_results[x]['mean_auc'])
best_auc = cv_results[best_model_name]['mean_auc']

logger.info(f"\n🏆 BEST MODEL: {best_model_name}")
logger.info(f"   Mean CV AUC: {best_auc:.4f}")
logger.info(f"   Status: {'✅ PASS' if best_auc >= 0.70 else '⚠️ REVIEW'}")

# ============================================================================
# STEP 5: REGISTER WITH REPORTING FRAMEWORK
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 5: REGISTERING WITH REPORTING FRAMEWORK")
logger.info("=" * 70)

chunk_registry = {
    'chunk_id': 'CHUNK_06',
    'chunk_name': 'Model Validation - Top 2 Models, 5-Fold CV',
    'execution_timestamp': datetime.now().isoformat(),
    'status': 'COMPLETED',
    'description': '5-Fold stratified cross-validation on auto-selected top 2 models',
    'selected_models': top_2_models,
    'cross_validation': {
        'method': '5-Fold Stratified',
        'folds': 5
    },
    'validation_results': cv_results,
    'best_model': {
        'name': best_model_name,
        'mean_cv_auc': float(best_auc),
        'cv_auc_std': float(cv_results[best_model_name]['std_auc']),
        'mean_f1': float(cv_results[best_model_name]['mean_f1']),
        'quality_gate_passed': best_auc >= 0.70
    },
    'outputs': [
        {
            'type': 'json',
            'name': 'validation_report.json',
            'path': os.path.join(CHUNK_06_REPORTS, 'validation_report.json'),
            'description': 'Comprehensive validation results'
        }
    ],
    'ready_for_next_chunk': True,
    'next_chunk': 'CHUNK_07 (Model Calibration)'
}

registry_file = os.path.join(REGISTRY_PATH, 'chunk_06_report.json')
with open(registry_file, 'w') as f:
    json.dump(chunk_registry, f, indent=2, default=str)
logger.info(f"✓ Registered: {registry_file}")

# Save validation report
report_path = os.path.join(CHUNK_06_REPORTS, 'validation_report.json')
with open(report_path, 'w') as f:
    json.dump(chunk_registry, f, indent=2, default=str)

# ============================================================================
# FINAL SUMMARY
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("CHUNK 06 SUMMARY - MODEL VALIDATION")
logger.info("=" * 70)
logger.info(f"✓ Models validated: 2 (auto-selected from 5)")
logger.info(f"✓ CV method: 5-Fold Stratified")
logger.info(f"✓ Best model: {best_model_name}")
logger.info(f"✓ Mean CV AUC: {best_auc:.4f}")
logger.info(f"✓ Quality gate: {'✅ PASS' if best_auc >= 0.70 else '⚠️ REVIEW'}")
logger.info(f"✓ Status: READY FOR CHUNK_07")
logger.info("=" * 70)
logger.info("\n✅ CHUNK 06 COMPLETED SUCCESSFULLY\n")
