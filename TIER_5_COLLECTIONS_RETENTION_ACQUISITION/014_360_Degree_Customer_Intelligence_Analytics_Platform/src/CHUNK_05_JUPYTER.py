#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CHUNK_05: MODEL SELECTION & TRAINING - JUPYTER VERSION (OPTIMIZED - SVM REMOVED)
================================================================================

Optimized version for FAST execution:
- SVM REMOVED (too slow)
- 3 faster models only
- Cross-validation: 3 folds (instead of 5)
- Execution time: 3-5 minutes (instead of 1+ hour)

Copy and paste each cell into your Jupyter notebook.

================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

print("\n" + "=" * 80)
print("CHUNK_05: MODEL SELECTION & TRAINING (OPTIMIZED - SVM REMOVED)")
print("=" * 80 + "\n")

# ============================================================================
# CELL 1: QUALITY GATE 1 - MODEL SELECTION (3 FAST MODELS)
# ============================================================================

print("=" * 80)
print("QUALITY GATE 1: MODEL SELECTION (3 FAST MODELS)")
print("=" * 80 + "\n")

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
}

print(f"[OK] Selected {len(models)} FAST models for classification:")
for model_name in models.keys():
    print(f"  - {model_name}")
print("[INFO] SVM REMOVED (too slow on large datasets)\n")

# ============================================================================
# CELL 2: QUALITY GATE 2 - DATA PREPARATION
# ============================================================================

print("=" * 80)
print("QUALITY GATE 2: DATA PREPARATION FOR MODELING")
print("=" * 80 + "\n")

# Find and prepare data
engineered = chunk04_results['engineered_datasets']
primary_dataset = None

for filename, df in engineered.items():
    if 'train' in filename.lower() and 'application' in filename.lower():
        primary_dataset = df
        dataset_name = filename
        break

if primary_dataset is None:
    print("[ERROR] Could not find application_train dataset!")
else:
    print(f"Using dataset: {dataset_name}")
    print(f"Shape: {primary_dataset.shape}")

    # Get TARGET from chunk04_results
    if 'targets_dict' in chunk04_results and dataset_name in chunk04_results['targets_dict']:
        y = chunk04_results['targets_dict'][dataset_name].copy()
        print(f"[OK] Got TARGET from chunk04_results")
    else:
        print(f"[ERROR] Could not find TARGET!")
        y = None

    if y is not None:
        X = primary_dataset

        # Handle data types and missing values
        valid_idx = y.notna()
        X = X[valid_idx]
        y = y[valid_idx]
        y = y.astype(int)

        print(f"\n[OK] Prepared data: X={X.shape}, y={y.shape}")
        print(f"  Classes: {len(np.unique(y))}")

        class_dist = dict(zip(*np.unique(y, return_counts=True)))
        print(f"  Class distribution: {class_dist}\n")

# ============================================================================
# CELL 3: QUALITY GATE 3 - MODEL TRAINING (3 FOLDS - FAST)
# ============================================================================

print("=" * 80)
print("QUALITY GATE 3: MODEL TRAINING WITH CROSS-VALIDATION (3-FOLD - FAST)")
print("=" * 80 + "\n")

trained_models = {}
training_results = {}

for model_name, model in models.items():
    print(f"Training: {model_name}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train
    model.fit(X_train, y_train)
    trained_models[model_name] = model

    # Cross-validation (3 FOLDS FOR SPEED)
    cv_scores = cross_val_score(model, X_train, y_train, cv=3, scoring='accuracy', n_jobs=-1)

    # Predictions
    y_pred = model.predict(X_test)

    # Store
    training_results[model_name] = {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'y_pred': y_pred,
        'cv_scores': cv_scores,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }

    print(f"  [OK] CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    print(f"  Train/Test: {len(y_train)}/{len(y_test)}\n")

# ============================================================================
# CELL 4: QUALITY GATE 4 - MODEL EVALUATION
# ============================================================================

print("=" * 80)
print("QUALITY GATE 4: MODEL EVALUATION")
print("=" * 80 + "\n")

evaluation_results = {}

for model_name, results in training_results.items():
    print(f"Evaluating: {model_name}")

    y_test = results['y_test']
    y_pred = results['y_pred']

    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
        'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
        'f1': f1_score(y_test, y_pred, average='weighted', zero_division=0)
    }

    evaluation_results[model_name] = metrics

    print(f"  Accuracy: {metrics['accuracy']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall: {metrics['recall']:.4f}")
    print(f"  F1 Score: {metrics['f1']:.4f}\n")

# ============================================================================
# CELL 5: QUALITY GATE 5 - FEATURE IMPORTANCE (TOP 10 ONLY)
# ============================================================================

print("=" * 80)
print("QUALITY GATE 5: FEATURE IMPORTANCE ANALYSIS (TOP 10 FEATURES)")
print("=" * 80 + "\n")

feature_importance = {}

for model_name, model in trained_models.items():
    print(f"Analyzing: {model_name}")

    importance = None

    # Tree-based models
    if hasattr(model, 'feature_importances_'):
        importance = model.feature_importances_
    elif hasattr(model, 'coef_'):
        importance = np.abs(model.coef_[0] if model.coef_.ndim > 1 else model.coef_)

    if importance is not None:
        importance_df = pd.DataFrame({
            'feature': X.columns,
            'importance': importance
        }).sort_values('importance', ascending=False).head(10)  # TOP 10 ONLY

        feature_importance[model_name] = importance_df

        print(f"  Top 5 features:")
        for idx, row in importance_df.head(5).iterrows():
            print(f"    - {row['feature']}: {row['importance']:.4f}")
    else:
        print(f"  [INFO] No feature importance available")

    print()

# ============================================================================
# CELL 6: QUALITY GATE 6 - MODEL COMPARISON
# ============================================================================

print("=" * 80)
print("QUALITY GATE 6: MODEL COMPARISON & RANKING")
print("=" * 80 + "\n")

# Rank by accuracy (FIXED: use reverse=True not ascending=False)
model_ranking = sorted(
    evaluation_results.items(),
    key=lambda x: x[1]['accuracy'],
    reverse=True
)

print("Model Rankings (by Accuracy):")
for rank, (model_name, metrics) in enumerate(model_ranking, 1):
    print(f"  {rank}. {model_name}: {metrics['accuracy']:.4f}")

best_model_name = model_ranking[0][0] if model_ranking else None
print(f"\n[OK] Best model: {best_model_name}\n")

# ============================================================================
# CELL 7: GENERATE SUMMARY
# ============================================================================

print("=" * 80)
print("GENERATING SUMMARY REPORT")
print("=" * 80 + "\n")

summary = "=" * 80 + "\n"
summary += "MODEL SELECTION & TRAINING SUMMARY (OPTIMIZED)\n"
summary += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
summary += "=" * 80 + "\n\n"

summary += "OPTIMIZATION APPLIED:\n"
summary += "✓ SVM REMOVED (too slow on large datasets)\n"
summary += "✓ Cross-validation: 3 folds (instead of 5)\n"
summary += "✓ Parallel processing enabled (n_jobs=-1)\n"
summary += "✓ Top 10 features analyzed\n"
summary += "✓ Expected execution time: 3-5 minutes\n\n"

summary += f"Dataset: {dataset_name}\n"
summary += f"Samples: {len(X)}\n"
summary += f"Features: {X.shape[1]}\n"
summary += f"Classes: {len(np.unique(y))}\n\n"

summary += "Models Trained:\n"
for model_name in models.keys():
    summary += f"  - {model_name}\n"

summary += "\nPerformance Summary:\n"
for model_name, metrics in evaluation_results.items():
    summary += f"\n{model_name}:\n"
    summary += f"  Accuracy: {metrics['accuracy']:.4f}\n"
    summary += f"  Precision: {metrics['precision']:.4f}\n"
    summary += f"  Recall: {metrics['recall']:.4f}\n"
    summary += f"  F1 Score: {metrics['f1']:.4f}\n"

summary += f"\nBest Model: {best_model_name}\n"
summary += "=" * 80 + "\n"

print(summary)

# ============================================================================
# CELL 8: STORE RESULTS
# ============================================================================

print("=" * 80)
print("CHUNK_05: MODEL SELECTION & TRAINING COMPLETE (OPTIMIZED)")
print("=" * 80 + "\n")

chunk05_results = {
    'models': models,
    'trained_models': trained_models,
    'training_results': training_results,
    'evaluation_results': evaluation_results,
    'feature_importance': feature_importance,
    'best_model': best_model_name,
    'best_model_object': trained_models.get(best_model_name),
    'summary': summary,
    'dataset_name': dataset_name,
    'X_shape': X.shape,
    'y_shape': y.shape
}

print("✓ Results stored in 'chunk05_results'")
print("✓ Ready for CHUNK_06 - Model Validation & Backtesting\n")

print("Execution time: 3-5 minutes (SVM removed, optimized)\n")
