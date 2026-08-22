"""
Pytest Configuration
Fixtures for all tests
"""

import pytest
import numpy as np
import pandas as pd

@pytest.fixture(scope='session')
def model():
    """Provide model to tests"""
    return best_model_obj

@pytest.fixture(scope='session')
def scaler_fixture():
    """Provide scaler to tests"""
    return scaler

@pytest.fixture(scope='session')
def features():
    """Provide features to tests"""
    return numeric_features

@pytest.fixture(scope='session')
def X_train():
    """Provide training data"""
    return X_train_scaled

@pytest.fixture(scope='session')
def X_test():
    """Provide test data"""
    return X_test_scaled

@pytest.fixture(scope='session')
def y_train():
    """Provide training target"""
    return y_train

@pytest.fixture(scope='session')
def y_test():
    """Provide test target"""
    return y_test
