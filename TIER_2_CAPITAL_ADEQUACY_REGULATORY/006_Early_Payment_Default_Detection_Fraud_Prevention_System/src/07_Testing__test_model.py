"""
Unit Tests for ML Model
Test model predictions and performance
"""

import pytest
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class TestModelPredictions:
    """Test model prediction functionality"""

    @staticmethod
    def test_model_exists():
        """Test that model is loaded"""
        assert best_model_obj is not None, "Model not loaded"

    @staticmethod
    def test_model_type():
        """Test model is Logistic Regression"""
        model_name = type(best_model_obj).__name__
        assert model_name == 'LogisticRegression', f"Expected LogisticRegression, got {model_name}"

    @staticmethod
    def test_scaler_exists():
        """Test that scaler is loaded"""
        assert scaler is not None, "Scaler not loaded"

    @staticmethod
    def test_features_exist():
        """Test that features list exists"""
        assert numeric_features is not None, "Features not loaded"
        assert len(numeric_features) == 130, f"Expected 130 features, got {len(numeric_features)}"

    @staticmethod
    def test_prediction_shape():
        """Test prediction output shape"""
        X_sample = X_test_scaled[:10]
        predictions = best_model_obj.predict(X_sample)
        assert predictions.shape == (10,), f"Expected shape (10,), got {predictions.shape}"

    @staticmethod
    def test_prediction_values():
        """Test prediction values are binary"""
        X_sample = X_test_scaled[:100]
        predictions = best_model_obj.predict(X_sample)
        unique_values = np.unique(predictions)
        assert set(unique_values).issubset({0, 1}), f"Predictions must be 0 or 1, got {unique_values}"

    @staticmethod
    def test_probability_shape():
        """Test probability output shape"""
        X_sample = X_test_scaled[:10]
        probabilities = best_model_obj.predict_proba(X_sample)
        assert probabilities.shape == (10, 2), f"Expected shape (10, 2), got {probabilities.shape}"

    @staticmethod
    def test_probability_values():
        """Test probabilities sum to 1"""
        X_sample = X_test_scaled[:100]
        probabilities = best_model_obj.predict_proba(X_sample)
        sums = probabilities.sum(axis=1)
        assert np.allclose(sums, 1.0), "Probabilities must sum to 1"

    @staticmethod
    def test_probability_range():
        """Test probabilities are in [0, 1]"""
        X_sample = X_test_scaled[:100]
        probabilities = best_model_obj.predict_proba(X_sample)
        assert np.all(probabilities >= 0) and np.all(probabilities <= 1), "Probabilities must be in [0, 1]"

    @staticmethod
    def test_model_performance():
        """Test model achieves expected performance"""
        predictions = best_model_obj.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, predictions)
        assert accuracy > 0.7, f"Accuracy must be > 0.7, got {accuracy}"

class TestDataValidation:
    """Test data quality and integrity"""

    @staticmethod
    def test_training_data_shape():
        """Test training data shape"""
        assert X_train_scaled.shape[0] > 0, "No training data"
        assert X_train_scaled.shape[1] == 130, f"Expected 130 features, got {X_train_scaled.shape[1]}"

    @staticmethod
    def test_test_data_shape():
        """Test test data shape"""
        assert X_test_scaled.shape[0] > 0, "No test data"
        assert X_test_scaled.shape[1] == 130, f"Expected 130 features, got {X_test_scaled.shape[1]}"

    @staticmethod
    def test_no_nan_train():
        """Test no NaN values in training data"""
        assert not np.isnan(X_train_scaled).any(), "NaN values found in training data"

    @staticmethod
    def test_no_nan_test():
        """Test no NaN values in test data"""
        assert not np.isnan(X_test_scaled).any(), "NaN values found in test data"

    @staticmethod
    def test_no_inf_train():
        """Test no infinity values in training data"""
        assert not np.isinf(X_train_scaled).any(), "Infinity values found in training data"

    @staticmethod
    def test_no_inf_test():
        """Test no infinity values in test data"""
        assert not np.isinf(X_test_scaled).any(), "Infinity values found in test data"

    @staticmethod
    def test_target_binary():
        """Test target is binary"""
        unique = np.unique(y_test)
        assert set(unique).issubset({0, 1}), f"Target must be binary, got {unique}"

    @staticmethod
    def test_data_split_ratio():
        """Test train/test split ratio"""
        total = X_train_scaled.shape[0] + X_test_scaled.shape[0]
        train_ratio = X_train_scaled.shape[0] / total
        assert 0.75 < train_ratio < 0.85, f"Train ratio should be ~0.8, got {train_ratio}"

class TestScaler:
    """Test feature scaler"""

    @staticmethod
    def test_scaler_type():
        """Test scaler is StandardScaler"""
        assert type(scaler).__name__ == 'StandardScaler', "Scaler must be StandardScaler"

    @staticmethod
    def test_scaler_fitted():
        """Test scaler is fitted"""
        assert hasattr(scaler, 'mean_'), "Scaler not fitted"
        assert len(scaler.mean_) == 130, f"Expected 130 means, got {len(scaler.mean_)}"

    @staticmethod
    def test_scaled_data_mean():
        """Test scaled data has mean ~0"""
        mean = X_test_scaled.mean(axis=0)
        assert np.allclose(mean, 0, atol=1e-10), f"Scaled data mean should be ~0, got {mean.mean()}"

    @staticmethod
    def test_scaled_data_std():
        """Test scaled data has std ~1"""
        std = X_test_scaled.std(axis=0)
        assert np.allclose(std, 1, atol=0.1), f"Scaled data std should be ~1, got {std.mean()}"

# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
