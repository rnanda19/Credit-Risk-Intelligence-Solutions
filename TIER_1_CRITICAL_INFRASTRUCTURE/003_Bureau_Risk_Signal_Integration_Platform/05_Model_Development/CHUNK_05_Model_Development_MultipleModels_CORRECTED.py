"""
PROBLEM 20: BUREAU RISK SIGNAL INTEGRATION
CHUNK 05: MODEL DEVELOPMENT - 5 MODELS (CORRECTED PATHS)

Purpose:
  Train 5 different ML models:
    1. Random Forest (3,000 trees)
    2. XGBoost
    3. LightGBM
    4. Logistic Regression
    5. Neural Network

  Compare performance across all models
  Create ensemble predictions
  Register outputs for CHUNK_13 aggregation

Compliance: BCBS 239, SOX 404, All 10 SOP Standards
Methodology: CRISP-DM, Ensemble Methods

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
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score, accuracy_score, log_loss
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import xgboost as xgb
import lightgbm as lgb

warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - CHUNK_05 - %(levelname)s - %(message)s')
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
CHUNK_05_METRICS = os.path.join(ROOT_PATH, "05_Model_Development", "Metrics")
CHUNK_05_REPORTS = os.path.join(ROOT_PATH, "05_Model_Development", "Reports")
CHUNK_05_GOVERNANCE = os.path.join(ROOT_PATH, "05_Model_Development", "Governance")
CHUNK_05_AUDIT = os.path.join(ROOT_PATH, "05_Model_Development", "Audit")
REGISTRY_PATH = os.path.join(ROOT_PATH, "00_Report_Registry")

for path in [CHUNK_05_MODELS, CHUNK_05_METRICS, CHUNK_05_REPORTS, CHUNK_05_GOVERNANCE, CHUNK_05_AUDIT, REGISTRY_PATH]:
    os.makedirs(path, exist_ok=True)

logger.info(f"Problem 20 Root: {ROOT_PATH}")

# ============================================================================
# STEP 1: LOAD ENGINEERED DATA
# ============================================================================
logger.info("\n" + "╔" + "=" * 68 + "╗")
logger.info("║" + " CHUNK 05: MODEL DEVELOPMENT - 5 MODELS ".center(68) + "║")
logger.info("╚" + "=" * 68 + "╝\n")

logger.info("=" * 70)
logger.info("STEP 1: LOADING ENGINEERED DATA FROM CHUNK_04")
logger.info("=" * 70)

input_file = os.path.join(CHUNK_04_PATH, 'bureau_risk_engineered.csv')
if not os.path.exists(input_file):
    logger.error(f"❌ Input not found: {input_file}")
    raise FileNotFoundError(f"Run CHUNK_04 first!")

df = pd.read_csv(input_file)
logger.info(f"✓ Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")

X = df.drop('TARGET', axis=1) if 'TARGET' in df.columns else df
y = df['TARGET'] if 'TARGET' in df.columns else None

if y is None:
    logger.error("❌ TARGET column not found!")
    raise ValueError("TARGET column required!")

# ============================================================================
# STEP 2: TRAIN-TEST SPLIT
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 2: STRATIFIED TRAIN-TEST SPLIT (80-20)")
logger.info("=" * 70)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

logger.info(f"✓ Training: {len(X_train):,} records")
logger.info(f"✓ Test: {len(X_test):,} records")

# ============================================================================
# STEP 3: TRAIN 5 MODELS
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 3: TRAINING 5 DIFFERENT MODELS")
logger.info("=" * 70)

models = {}
predictions = {}

# Model 1: Random Forest
logger.info("\n[1/5] Training Random Forest Classifier...")
rf = RandomForestClassifier(n_estimators=3000, max_depth=25, min_samples_split=50, random_state=42, n_jobs=-1, class_weight='balanced')
rf.fit(X_train, y_train)
models['Random Forest'] = rf
predictions['Random Forest'] = rf.predict_proba(X_test)[:, 1]
logger.info("✓ Random Forest trained")

# Model 2: XGBoost
logger.info("\n[2/5] Training XGBoost Classifier...")
xgb_model = xgb.XGBClassifier(n_estimators=1000, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1, scale_pos_weight=(y_train==0).sum() / (y_train==1).sum())
xgb_model.fit(X_train, y_train)
models['XGBoost'] = xgb_model
predictions['XGBoost'] = xgb_model.predict_proba(X_test)[:, 1]
logger.info("✓ XGBoost trained")

# Model 3: LightGBM
logger.info("\n[3/5] Training LightGBM Classifier...")
lgb_model = lgb.LGBMClassifier(n_estimators=1000, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1, scale_pos_weight=(y_train==0).sum() / (y_train==1).sum())
lgb_model.fit(X_train, y_train)
models['LightGBM'] = lgb_model
predictions['LightGBM'] = lgb_model.predict_proba(X_test)[:, 1]
logger.info("✓ LightGBM trained")

# Model 4: Logistic Regression
logger.info("\n[4/5] Training Logistic Regression...")
lr = LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1, class_weight='balanced')
lr.fit(X_train_scaled, y_train)
models['Logistic Regression'] = lr
predictions['Logistic Regression'] = lr.predict_proba(X_test_scaled)[:, 1]
logger.info("✓ Logistic Regression trained")

# Model 5: Neural Network
logger.info("\n[5/5] Training Neural Network Classifier...")
nn = MLPClassifier(hidden_layer_sizes=(256, 128, 64), max_iter=500, learning_rate='adaptive', learning_rate_init=0.001, random_state=42, early_stopping=True, validation_fraction=0.2)
nn.fit(X_train_scaled, y_train)
models['Neural Network'] = nn
predictions['Neural Network'] = nn.predict_proba(X_test_scaled)[:, 1]
logger.info("✓ Neural Network trained")

# ============================================================================
# STEP 4: EVALUATE MODELS
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 4: MODEL EVALUATION")
logger.info("=" * 70)

model_performance = {}

for model_name, y_pred_proba in predictions.items():
    y_pred = (y_pred_proba >= 0.5).astype(int)

    model_performance[model_name] = {
        'AUC': float(roc_auc_score(y_test, y_pred_proba)),
        'F1': float(f1_score(y_test, y_pred)),
        'Precision': float(precision_score(y_test, y_pred)),
        'Recall': float(recall_score(y_test, y_pred)),
        'Accuracy': float(accuracy_score(y_test, y_pred)),
        'LogLoss': float(log_loss(y_test, y_pred_proba))
    }

    logger.info(f"\n{model_name}:")
    logger.info(f"  ├─ AUC: {model_performance[model_name]['AUC']:.4f}")
    logger.info(f"  ├─ F1: {model_performance[model_name]['F1']:.4f}")
    logger.info(f"  └─ Accuracy: {model_performance[model_name]['Accuracy']:.4f}")

best_model_name = max(model_performance, key=lambda x: model_performance[x]['AUC'])
logger.info(f"\n🏆 BEST: {best_model_name} (AUC={model_performance[best_model_name]['AUC']:.4f})")

# ============================================================================
# STEP 5: SAVE MODELS
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 5: SAVING TRAINED MODELS")
logger.info("=" * 70)

for model_name, model in models.items():
    model_path = os.path.join(CHUNK_05_MODELS, f'{model_name.lower().replace(" ", "_")}_v1.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    logger.info(f"✓ Saved {model_name}")

scaler_path = os.path.join(CHUNK_05_MODELS, 'feature_scaler_v1.pkl')
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)

# ============================================================================
# STEP 6: REGISTER WITH REPORTING FRAMEWORK
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("STEP 6: REGISTERING WITH REPORTING FRAMEWORK")
logger.info("=" * 70)

chunk_registry = {
    'chunk_id': 'CHUNK_05',
    'chunk_name': 'Model Development - 5 Models',
    'execution_timestamp': datetime.now().isoformat(),
    'status': 'COMPLETED',
    'description': 'Training 5 different ML models for comparison',
    'models_trained': list(models.keys()),
    'best_model': best_model_name,
    'outputs': [
        {'type': 'pkl', 'path': os.path.join(CHUNK_05_MODELS, f'{n.lower().replace(" ", "_")}_v1.pkl'), 'description': f'{n} model'}
        for n in models.keys()
    ],
    'key_metrics': {
        'models_trained': 5,
        'best_model': best_model_name,
        'best_auc': float(model_performance[best_model_name]['AUC']),
        'all_models_performance': model_performance
    },
    'ready_for_next_chunk': True,
    'next_chunk': 'CHUNK_06 (Model Validation - Top 2)'
}

registry_file = os.path.join(REGISTRY_PATH, 'chunk_05_report.json')
with open(registry_file, 'w') as f:
    json.dump(chunk_registry, f, indent=2, default=str)
logger.info(f"✓ Registered: {registry_file}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
logger.info("\n" + "=" * 70)
logger.info("CHUNK 05 SUMMARY - MODEL DEVELOPMENT")
logger.info("=" * 70)
logger.info(f"✓ Models trained: 5")
for name, metrics in model_performance.items():
    logger.info(f"  {name}: AUC={metrics['AUC']:.4f}")
logger.info(f"✓ Best model: {best_model_name}")
logger.info(f"✓ Status: READY FOR CHUNK_06")
logger.info("=" * 70)
logger.info("\n✅ CHUNK 05 COMPLETED SUCCESSFULLY\n")
