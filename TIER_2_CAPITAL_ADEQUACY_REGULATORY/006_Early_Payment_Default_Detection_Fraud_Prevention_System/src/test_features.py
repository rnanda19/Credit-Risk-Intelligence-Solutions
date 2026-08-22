"""
Unit Tests for Features
Test feature engineering and validity
"""

import pytest
import numpy as np
import pandas as pd

class TestFeatures:
    """Test feature set"""

    @staticmethod
    def test_feature_count():
        """Test expected number of features"""
        assert len(numeric_features) == 130, f"Expected 130 features, got {len(numeric_features)}"

    @staticmethod
    def test_feature_names_unique():
        """Test feature names are unique"""
        assert len(numeric_features) == len(set(numeric_features)), "Duplicate feature names found"

    @staticmethod
    def test_no_missing_values_in_features():
        """Test features have no missing values"""
        missing = df_features[numeric_features].isnull().sum().sum()
        assert missing == 0, f"Features have {missing} missing values"

    @staticmethod
    def test_features_numeric():
        """Test all features are numeric"""
        for feature in numeric_features:
            dtype = df_features[feature].dtype
            assert np.issubdtype(dtype, np.number), f"Feature {feature} is not numeric"

    @staticmethod
    def test_target_not_in_features():
        """Test TARGET is not in features"""
        assert 'TARGET' not in numeric_features, "TARGET should not be in features"

    @staticmethod
    def test_sk_id_not_in_features():
        """Test SK_ID_CURR is not in features"""
        assert 'SK_ID_CURR' not in numeric_features, "SK_ID_CURR should not be in features"

class TestFeatureStatistics:
    """Test feature statistical properties"""

    @staticmethod
    def test_feature_ranges():
        """Test features have reasonable ranges"""
        for feature in numeric_features[:10]:
            values = df_features[feature]
            assert values.min() > -1000, f"{feature} has unreasonable minimum"
            assert values.max() < 1000, f"{feature} has unreasonable maximum"

    @staticmethod
    def test_feature_std():
        """Test features have non-zero standard deviation"""
        for feature in numeric_features[:10]:
            std = df_features[feature].std()
            assert std > 0, f"{feature} has zero standard deviation"

    @staticmethod
    def test_feature_variance():
        """Test features have variance"""
        for feature in numeric_features[:10]:
            variance = df_features[feature].var()
            assert variance > 0, f"{feature} has zero variance"

# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
