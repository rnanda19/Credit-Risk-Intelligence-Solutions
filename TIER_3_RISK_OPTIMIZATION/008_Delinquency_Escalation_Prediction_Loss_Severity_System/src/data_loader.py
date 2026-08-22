"""
Data Loader Utilities for Problem 19
Loads cleaned and engineered features
"""
import pandas as pd
import os

def load_cleaned_data(base_path="02_Data_Cleaning_Preprocessing/Cleaned_Data/"):
    """Load cleaned application data"""
    file_path = os.path.join(base_path, "application_cleaned.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None

def load_engineered_features(base_path="05_Feature_Engineering/"):
    """Load engineered features (scaled)"""
    file_path = os.path.join(base_path, "features_engineered_scaled.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None

def load_selected_features(base_path="06_Feature_Selection/"):
    """Load final selected features (75 features)"""
    file_path = os.path.join(base_path, "features_selected.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None
