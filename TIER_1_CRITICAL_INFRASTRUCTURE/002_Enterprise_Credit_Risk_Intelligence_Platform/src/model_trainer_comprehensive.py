
import pickle
import logging
from pathlib import Path
import polars as pl
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostClassifier
import sys
sys.path.append(r"C:\Users\rnand\Documents\home-credit-default-risk\Enterprise_AI_Workflows\001_PD_Ultimate_Final")
from config import DATA_PROCESSED_DIR, MODELS_DIR, LOGS_DIR, RANDOM_STATE, TARGET_COL, ID_COL

logging.basicConfig(filename=LOGS_DIR / "model_trainer.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - [Trainer] - %(message)s')

def train_and_benchmark_all_models() -> None:
    print("Starting Comprehensive Model Training & Benchmarking Suite...")
    feature_path = DATA_PROCESSED_DIR / "master_features_engineered.parquet"
    df = pl.read_parquet(feature_path)

    drop_cols = [ID_COL, TARGET_COL]
    numeric_features = [col for col in df.columns if col not in drop_cols and df[col].dtype in [pl.Float32, pl.Float64, pl.Int32, pl.Int64]]

    X = df.select(numeric_features).fill_null(0).to_numpy()
    y = df.select(TARGET_COL).to_numpy().ravel()

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    models = {
        "Logistic Regression": LogisticRegression(max_iter=300, random_state=RANDOM_STATE),
        "Random Forest": RandomForestClassifier(n_estimators=50, max_depth=6, random_state=RANDOM_STATE),
        "XGBoost": xgb.XGBClassifier(n_estimators=50, learning_rate=0.05, max_depth=4, random_state=RANDOM_STATE, eval_metric='auc'),
        "CatBoost": CatBoostClassifier(iterations=50, learning_rate=0.05, depth=4, verbose=0, random_seed=RANDOM_STATE),
        "LightGBM": lgb.LGBMClassifier(n_estimators=50, learning_rate=0.05, max_depth=4, random_state=RANDOM_STATE, verbose=-1)
    }

    best_auc = 0.0
    best_model_name = None
    best_model_instance = None

    for name, model in models.items():
        fold_scores = []
        for train_idx, val_idx in cv.split(X, y):
            model.fit(X[train_idx], y[train_idx])
            preds = model.predict_proba(X[val_idx])[:, 1]
            fold_scores.append(roc_auc_score(y[val_idx], preds))
        mean_auc = np.mean(fold_scores)
        print(f"-> {name} | Mean CV AUC: {mean_auc:.4f}")

        if mean_auc > best_auc:
            best_auc = mean_auc
            best_model_name = name
            best_model_instance = model

    print(f"\n[CHAMPION] Ultimate Model Selected: {best_model_name} (AUC: {best_auc:.4f})")
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    with open(MODELS_DIR / "champion_pd_model.pkl", "wb") as f:
        pickle.dump(best_model_instance, f)
    print("[SUCCESS] Champion model serialized successfully.")
