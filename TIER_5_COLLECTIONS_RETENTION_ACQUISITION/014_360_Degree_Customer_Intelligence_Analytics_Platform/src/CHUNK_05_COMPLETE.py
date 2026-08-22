#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
CHUNK_05: MODEL SELECTION & TRAINING - OPTIMIZED (SVM REMOVED, FASTER)
================================================================================

Optimized version for FAST execution:
- SVM REMOVED (too slow on large datasets)
- 3 faster models only
- Cross-validation: 3 folds (instead of 5)
- Simplified feature importance
- Execution time: 3-5 minutes (instead of 1+ hour)

Uses real TARGET from application_train.csv.
Proper data type handling included.

USAGE IN JUPYTER:
    exec(open(r'CHUNK_05_MODEL_SELECTION/scripts/CHUNK_05_COMPLETE.py').read())

================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import warnings

warnings.filterwarnings('ignore')

print("\n" + "=" * 80)
print("CHUNK_05: MODEL SELECTION & TRAINING (OPTIMIZED - SVM REMOVED)")
print("=" * 80 + "\n")

# ============================================================================
# UTILITY CLASSES (Embedded)
# ============================================================================

class ModelSelector:
    """Select best algorithms"""

    def __init__(self):
        self.models = {}

    def select_for_classification(self):
        """Select FAST classification models (SVM removed)"""
        self.models = {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
        }
        return self.models


class ModelTrainer:
    """Train models with cross-validation"""

    def __init__(self):
        self.trained_models = {}
        self.training_results = {}

    def train_model(self, model, X, y, model_name='Model', cv=3):
        """Train single model with OPTIMIZED cv=3"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train
        model.fit(X_train, y_train)
        self.trained_models[model_name] = model

        # Cross-validation (3 folds for speed)
        cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='accuracy', n_jobs=-1)

        # Predictions
        y_pred = model.predict(X_test)

        # Store
        self.training_results[model_name] = {
            'X_train': X_train,
            'X_test': X_test,
            'y_train': y_train,
            'y_test': y_test,
            'y_pred': y_pred,
            'cv_scores': cv_scores,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }

        return model, cv_scores, y_pred


class ModelEvaluator:
    """Evaluate model performance"""

    def __init__(self):
        self.evaluation_results = {}

    def evaluate_classification(self, y_true, y_pred, model_name='Model'):
        """Evaluate classification"""
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
            'f1': f1_score(y_true, y_pred, average='weighted', zero_division=0)
        }

        self.evaluation_results[model_name] = metrics
        return metrics


class FeatureImportanceAnalyzer:
    """Extract feature importance"""

    def __init__(self):
        self.feature_importance = {}

    def extract_importance(self, model, feature_names, model_name='Model', top_n=10):
        """Extract importance (top 10 only for speed)"""
        importance = None

        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importance = np.abs(model.coef_[0] if model.coef_.ndim > 1 else model.coef_)

        if importance is not None:
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': importance
            }).sort_values('importance', ascending=False).head(top_n)

            self.feature_importance[model_name] = importance_df
            return importance_df

        return None


# ============================================================================
# MAIN EXECUTION FUNCTION
# ============================================================================

def run_chunk05(engineered_datasets):
    """
    Execute CHUNK_05 Model Selection & Training (OPTIMIZED)

    Args:
        engineered_datasets: Dictionary of engineered DataFrames from CHUNK_04

    Returns:
        Dictionary with trained models and results
    """

    print("=" * 80)
    print("QUALITY GATE 1: MODEL SELECTION (3 FAST MODELS)")
    print("=" * 80 + "\n")

    selector = ModelSelector()
    models = selector.select_for_classification()

    print(f"[OK] Selected {len(models)} FAST models for classification:")
    for model_name in models.keys():
        print(f"  - {model_name}")
    print("[INFO] SVM removed (too slow)\n")

    print("=" * 80)
    print("QUALITY GATE 2: DATA PREPARATION FOR MODELING")
    print("=" * 80 + "\n")

    # Use application_train as primary dataset
    primary_dataset = None
    dataset_name = None

    for filename, df in engineered_datasets.items():
        if 'train' in filename.lower() and 'application' in filename.lower():
            primary_dataset = df
            dataset_name = filename
            break

    if primary_dataset is None:
        print("[ERROR] Could not find application_train dataset!")
        return None

    print(f"Using dataset: {dataset_name}")
    print(f"Shape: {primary_dataset.shape}")

    # Get TARGET from chunk04_results
    target_values = None

    if 'chunk04_results' in globals() and 'targets_dict' in chunk04_results:
        if dataset_name in chunk04_results['targets_dict']:
            target_values = chunk04_results['targets_dict'][dataset_name].copy()

    if target_values is None:
        print("[ERROR] Could not find TARGET values!")
        return None

    X = primary_dataset
    y = target_values

    # Handle data types and missing values
    valid_idx = y.notna()
    X = X[valid_idx]
    y = y[valid_idx]
    y = y.astype(int)

    print(f"[OK] Prepared data: X={X.shape}, y={y.shape}")
    print(f"  Classes: {len(np.unique(y))}")

    class_dist = dict(zip(*np.unique(y, return_counts=True)))
    print(f"  Class distribution: {class_dist}\n")

    print("=" * 80)
    print("QUALITY GATE 3: MODEL TRAINING WITH CROSS-VALIDATION (3-FOLD - FAST)")
    print("=" * 80 + "\n")

    trainer = ModelTrainer()
    training_summary = {}

    for model_name, model in models.items():
        print(f"Training: {model_name}")

        try:
            trained_model, cv_scores, y_pred = trainer.train_model(
                model, X, y, model_name, cv=3  # OPTIMIZED: 3 folds instead of 5
            )

            training_summary[model_name] = {
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'cv_scores': cv_scores.tolist()
            }

            print(f"  [OK] CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
            print(f"  Train size: {len(trainer.training_results[model_name]['y_train'])}")
            print(f"  Test size: {len(trainer.training_results[model_name]['y_test'])}\n")

        except Exception as e:
            print(f"  [ERROR] {str(e)}\n")
            continue

    print("=" * 80)
    print("QUALITY GATE 4: MODEL EVALUATION")
    print("=" * 80 + "\n")

    evaluator = ModelEvaluator()
    evaluation_summary = {}

    for model_name, results in trainer.training_results.items():
        print(f"Evaluating: {model_name}")

        metrics = evaluator.evaluate_classification(
            results['y_test'], results['y_pred'], model_name
        )

        evaluation_summary[model_name] = metrics

        print(f"  Accuracy: {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall: {metrics['recall']:.4f}")
        print(f"  F1 Score: {metrics['f1']:.4f}\n")

    print("=" * 80)
    print("QUALITY GATE 5: FEATURE IMPORTANCE ANALYSIS (TOP 10 FEATURES)")
    print("=" * 80 + "\n")

    importance_analyzer = FeatureImportanceAnalyzer()
    feature_importance_summary = {}

    for model_name, model in trainer.trained_models.items():
        print(f"Analyzing: {model_name}")

        importance_df = importance_analyzer.extract_importance(
            model, X.columns, model_name, top_n=10  # OPTIMIZED: Top 10 only
        )

        if importance_df is not None:
            feature_importance_summary[model_name] = importance_df
            print(f"  Top 5 features:")
            for idx, row in importance_df.head(5).iterrows():
                print(f"    - {row['feature']}: {row['importance']:.4f}")
        else:
            print(f"  [INFO] No feature importance available")

        print()

    print("=" * 80)
    print("QUALITY GATE 6: MODEL COMPARISON & RANKING")
    print("=" * 80 + "\n")

    # Rank models by accuracy (FIXED: use reverse=True not ascending=False)
    model_ranking = sorted(
        evaluation_summary.items(),
        key=lambda x: x[1]['accuracy'],
        reverse=True
    )

    print("Model Rankings (by Accuracy):")
    for rank, (model_name, metrics) in enumerate(model_ranking, 1):
        print(f"  {rank}. {model_name}: {metrics['accuracy']:.4f}")

    best_model_name = model_ranking[0][0] if model_ranking else None
    print(f"\n[OK] Best model: {best_model_name}\n")

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
    for model_name, metrics in evaluation_summary.items():
        summary += f"\n{model_name}:\n"
        summary += f"  Accuracy: {metrics['accuracy']:.4f}\n"
        summary += f"  Precision: {metrics['precision']:.4f}\n"
        summary += f"  Recall: {metrics['recall']:.4f}\n"
        summary += f"  F1 Score: {metrics['f1']:.4f}\n"

    summary += f"\nBest Model: {best_model_name}\n"
    summary += "=" * 80 + "\n"

    print(summary)

    print("\n" + "=" * 80)
    print("CHUNK_05: MODEL SELECTION & TRAINING COMPLETE (OPTIMIZED)")
    print("=" * 80 + "\n")

    print("Ready for CHUNK_06 - Model Validation & Backtesting\n")

    return {
        'models': models,
        'trained_models': trainer.trained_models,
        'training_results': trainer.training_results,
        'evaluation_results': evaluator.evaluation_results,
        'feature_importance': importance_analyzer.feature_importance,
        'best_model': best_model_name,
        'best_model_object': trainer.trained_models.get(best_model_name),
        'summary': summary,
        'dataset_name': dataset_name,
        'X_shape': X.shape,
        'y_shape': y.shape
    }


# ============================================================================
# AUTO-RUN IF CHUNK_04 RESULTS AVAILABLE
# ============================================================================

if __name__ == '__main__' or 'chunk04_results' in globals():
    try:
        if 'chunk04_results' in globals():
            print("[OK] Found CHUNK_04 results\n")
            chunk05_results = run_chunk05(
                engineered_datasets=chunk04_results['engineered_datasets']
            )
        else:
            print("[INFO] CHUNK_04 results not found. Call manually:")
            print("    chunk05_results = run_chunk05(engineered_datasets=chunk04_results['engineered_datasets'])")
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        print("\n[INFO] To run manually, use:")
        print("    chunk05_results = run_chunk05(engineered_datasets=chunk04_results['engineered_datasets'])")
