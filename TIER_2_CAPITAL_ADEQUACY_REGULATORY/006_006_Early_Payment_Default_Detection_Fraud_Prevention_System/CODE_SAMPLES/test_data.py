"""
Unit Tests for Data Quality
Test data integrity, quality, and consistency
"""

import pytest
import numpy as np
import pandas as pd

class TestDataQuality:
    """Test overall data quality"""

    @staticmethod
    def test_dataset_not_empty():
        """Test dataset is not empty"""
        assert len(df_features) > 0, "Dataset is empty"

    @staticmethod
    def test_features_not_empty():
        """Test feature list is not empty"""
        assert len(df_features.columns) > 0, "No features in dataset"

    @staticmethod
    def test_target_exists():
        """Test target column exists"""
        assert 'TARGET' in df_features.columns, "TARGET column not found"

    @staticmethod
    def test_no_complete_duplicates():
        """Test no complete duplicate rows"""
        duplicates = df_features.duplicated().sum()
        assert duplicates == 0, f"Found {duplicates} duplicate rows"

    @staticmethod
    def test_unique_ids():
        """Test SK_ID_CURR is unique"""
        if 'SK_ID_CURR' in df_features.columns:
            duplicates = df_features['SK_ID_CURR'].duplicated().sum()
            assert duplicates == 0, f"Found {duplicates} duplicate IDs"

class TestMissingValues:
    """Test missing value handling"""

    @staticmethod
    def test_numeric_no_missing():
        """Test numeric columns have no missing values"""
        numeric_cols = df_features.select_dtypes(include=[np.number]).columns
        missing = df_features[numeric_cols].isnull().sum().sum()
        assert missing == 0, f"Found {missing} missing values in numeric columns"

    @staticmethod
    def test_categorical_no_missing():
        """Test categorical columns have no missing values"""
        categorical_cols = df_features.select_dtypes(include=['object']).columns
        missing = df_features[categorical_cols].isnull().sum().sum()
        assert missing == 0, f"Found {missing} missing values in categorical columns"

class TestOutliers:
    """Test outlier detection"""

    @staticmethod
    def test_reasonable_ranges():
        """Test numeric values are in reasonable ranges"""
        numeric_cols = df_features.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            values = df_features[col]
            q1 = values.quantile(0.25)
            q3 = values.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 10 * iqr
            upper = q3 + 10 * iqr
            out_of_range = ((values < lower) | (values > upper)).sum()
            assert out_of_range < len(df_features) * 0.1, f"Too many outliers in {col}"

class TestTargetDistribution:
    """Test target variable distribution"""

    @staticmethod
    def test_target_balance():
        """Test target class distribution"""
        target_counts = df_features['TARGET'].value_counts()
        ratio = min(target_counts.values) / max(target_counts.values)
        assert ratio > 0.05, f"Classes too imbalanced, ratio: {ratio}"

    @staticmethod
    def test_target_no_missing():
        """Test target has no missing values"""
        missing = df_features['TARGET'].isnull().sum()
        assert missing == 0, f"TARGET has {missing} missing values"

# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
