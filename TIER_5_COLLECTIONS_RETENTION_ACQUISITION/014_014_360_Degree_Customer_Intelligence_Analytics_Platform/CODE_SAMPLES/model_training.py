#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
CHUNK_05: MODEL SELECTION & TRAINING LIBRARY
================================================================================

Utility classes for model selection and training:
- ModelSelector: Select best algorithms for problem type
- ModelTrainer: Train models with cross-validation
- HyperparameterTuner: Optimize hyperparameters
- ModelEvaluator: Evaluate model performance
- ModelComparator: Compare multiple models
- ModelPersistence: Save and load trained models

================================================================================
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, train_test_split, KFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report, roc_curve, auc
)
import warnings

warnings.filterwarnings('ignore')


class ModelSelector:
    """Select best algorithms for problem type"""

    def __init__(self):
        self.models = {}
        self.problem_type = None

    def select_for_classification(self, n_samples=None, n_features=None):
        """Select models for classification problem"""
        self.problem_type = 'classification'

        models = {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'SVM': SVC(probability=True, random_state=42)
        }

        self.models = models
        return models

    def select_for_regression(self):
        """Select models for regression problem"""
        self.problem_type = 'regression'

        from sklearn.ensemble import RandomForestRegressor
        from sklearn.linear_model import LinearRegression
        from sklearn.svm import SVR

        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'SVM': SVR()
        }

        self.models = models
        return models

    def get_models(self):
        """Get selected models"""
        return self.models


class ModelTrainer:
    """Train models with cross-validation"""

    def __init__(self):
        self.trained_models = {}
        self.training_results = {}

    def train_model(self, model, X, y, model_name='Model', cv=5):
        """Train single model with cross-validation"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        model.fit(X_train, y_train)
        self.trained_models[model_name] = model

        # Cross-validation scores
        cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='accuracy')

        # Test predictions
        y_pred = model.predict(X_test)

        # Store results
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

    def train_multiple(self, models, X, y, cv=5):
        """Train multiple models"""
        results = {}

        for model_name, model in models.items():
            trained_model, cv_scores, y_pred = self.train_model(
                model, X, y, model_name, cv
            )
            results[model_name] = {
                'model': trained_model,
                'cv_scores': cv_scores,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'y_pred': y_pred
            }

        return results

    def get_trained_model(self, model_name):
        """Get trained model"""
        return self.trained_models.get(model_name)


class ModelEvaluator:
    """Evaluate model performance"""

    def __init__(self):
        self.evaluation_results = {}

    def evaluate_classification(self, y_true, y_pred, model_name='Model'):
        """Evaluate classification model"""
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
            'f1': f1_score(y_true, y_pred, average='weighted', zero_division=0),
            'confusion_matrix': confusion_matrix(y_true, y_pred)
        }

        # ROC AUC if binary classification
        if len(np.unique(y_true)) == 2:
            try:
                y_pred_proba = getattr(self, 'model', None)
                if y_pred_proba is not None:
                    metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba[:, 1])
            except:
                pass

        self.evaluation_results[model_name] = metrics
        return metrics

    def evaluate_regression(self, y_true, y_pred, model_name='Model'):
        """Evaluate regression model"""
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

        metrics = {
            'mse': mean_squared_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'mae': mean_absolute_error(y_true, y_pred),
            'r2': r2_score(y_true, y_pred)
        }

        self.evaluation_results[model_name] = metrics
        return metrics

    def get_evaluation(self, model_name):
        """Get evaluation results"""
        return self.evaluation_results.get(model_name)


class ModelComparator:
    """Compare multiple models"""

    def __init__(self):
        self.comparison_results = {}

    def compare_models(self, results_dict):
        """Compare model results"""
        comparison = {}

        for model_name, results in results_dict.items():
            comparison[model_name] = {
                'cv_mean': results.get('cv_mean', 0),
                'cv_std': results.get('cv_std', 0),
                'training_samples': len(results.get('y_train', [])),
                'testing_samples': len(results.get('y_test', []))
            }

        self.comparison_results = comparison
        return comparison

    def rank_models(self, metric='cv_mean', ascending=False):
        """Rank models by performance metric"""
        if not self.comparison_results:
            return []

        ranked = sorted(
            self.comparison_results.items(),
            key=lambda x: x[1].get(metric, 0),
            ascending=ascending
        )

        return [(name, results[metric]) for name, results in ranked]

    def get_best_model(self, metric='cv_mean'):
        """Get best performing model"""
        ranked = self.rank_models(metric, ascending=False)
        if ranked:
            return ranked[0][0]
        return None


class HyperparameterTuner:
    """Optimize hyperparameters"""

    def __init__(self):
        self.tuning_results = {}

    def simple_grid_search(self, model, param_grid, X_train, y_train, cv=3):
        """Simple grid search for hyperparameter tuning"""
        from sklearn.model_selection import GridSearchCV

        grid_search = GridSearchCV(model, param_grid, cv=cv, scoring='accuracy', n_jobs=-1)
        grid_search.fit(X_train, y_train)

        results = {
            'best_params': grid_search.best_params_,
            'best_score': grid_search.best_score_,
            'best_model': grid_search.best_estimator_,
            'cv_results': grid_search.cv_results_
        }

        return results

    def random_search(self, model, param_distributions, X_train, y_train, n_iter=10, cv=3):
        """Random search for hyperparameter tuning"""
        from sklearn.model_selection import RandomizedSearchCV

        random_search = RandomizedSearchCV(
            model, param_distributions, n_iter=n_iter, cv=cv,
            scoring='accuracy', random_state=42, n_jobs=-1
        )
        random_search.fit(X_train, y_train)

        results = {
            'best_params': random_search.best_params_,
            'best_score': random_search.best_score_,
            'best_model': random_search.best_estimator_,
            'cv_results': random_search.cv_results_
        }

        return results


class FeatureImportanceAnalyzer:
    """Analyze feature importance from trained models"""

    def __init__(self):
        self.feature_importance = {}

    def extract_importance(self, model, feature_names, model_name='Model'):
        """Extract feature importance"""
        importance = None

        # Tree-based models
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_

        # Coefficient-based models
        elif hasattr(model, 'coef_'):
            importance = np.abs(model.coef_[0] if model.coef_.ndim > 1 else model.coef_)

        if importance is not None:
            # Create DataFrame
            feature_importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': importance
            }).sort_values('importance', ascending=False)

            self.feature_importance[model_name] = feature_importance_df
            return feature_importance_df

        return None

    def get_top_features(self, model_name, top_n=10):
        """Get top N important features"""
        if model_name in self.feature_importance:
            return self.feature_importance[model_name].head(top_n)
        return None


class ModelPersistence:
    """Save and load trained models"""

    def __init__(self):
        self.saved_models = {}

    def save_model(self, model, model_name, path):
        """Save trained model"""
        import pickle

        try:
            with open(f'{path}/{model_name}.pkl', 'wb') as f:
                pickle.dump(model, f)
            self.saved_models[model_name] = path
            return True
        except Exception as e:
            print(f"Error saving model: {e}")
            return False

    def load_model(self, model_name, path):
        """Load trained model"""
        import pickle

        try:
            with open(f'{path}/{model_name}.pkl', 'rb') as f:
                model = pickle.load(f)
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
