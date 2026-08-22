#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
CHUNK_04: FEATURE ENGINEERING - COMPLETE VERSION (DATA LEAKAGE FIXED)
================================================================================

Complete standalone version that works in Jupyter notebooks.
NO SYNTHETIC DATA - Uses real CSV datasets only.
DATA LEAKAGE FIXED - TARGET removed before feature engineering.

USAGE IN JUPYTER:
    %cd "path/to/CHUNK_04_FEATURE_ENGINEERING"
    exec(open('scripts/CHUNK_04_COMPLETE.py').read())

Then call:
    chunk04_results = run_chunk04(cleaned_datasets)

================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import warnings

warnings.filterwarnings('ignore')

print("\n" + "=" * 80)
print("CHUNK_04: FEATURE ENGINEERING (DATA LEAKAGE FIXED)")
print("=" * 80 + "\n")

# ============================================================================
# UTILITY CLASSES (Embedded)
# ============================================================================

class CategoricalEncoder:
    """Encode categorical variables"""

    def __init__(self):
        self.encoding_mapping = {}

    def label_encode(self, df, columns):
        """Label encode categorical columns"""
        new_df = df.copy()

        for col in columns:
            if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                unique_values = df[col].dropna().unique()
                mapping = {val: idx for idx, val in enumerate(unique_values)}
                new_df[col] = df[col].map(mapping)
                self.encoding_mapping[col] = mapping

        return new_df


class FeatureTransformer:
    """Transform features"""

    def __init__(self):
        self.scalers = {}

    def standardize(self, df, columns):
        """Standardize features (z-score)"""
        new_df = df.copy()
        scaler = StandardScaler()

        numeric_cols = [c for c in columns if pd.api.types.is_numeric_dtype(df[c])]
        if numeric_cols:
            new_df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
            self.scalers['standard'] = scaler

        return new_df


class FeatureQualityAssessor:
    """Assess engineered features"""

    def __init__(self):
        pass

    def assess_features(self, df, original_df):
        """Assess feature quality"""
        assessment = {
            'total_original': len(original_df.columns),
            'total_new': len(df.columns),
            'features_added': len(df.columns) - len(original_df.columns),
            'memory_increase_mb': round(
                (df.memory_usage(deep=True).sum() -
                 original_df.memory_usage(deep=True).sum()) / (1024**2), 2
            )
        }
        return assessment

    def detect_redundant_features(self, df, threshold=0.95):
        """Detect redundant features"""
        numeric_df = df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr()

        redundant_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > threshold:
                    redundant_pairs.append((
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        round(corr_matrix.iloc[i, j], 4)
                    ))

        return redundant_pairs


# ============================================================================
# MAIN EXECUTION FUNCTION
# ============================================================================

def run_chunk04(cleaned_datasets, chunk03_results=None):
    """
    Execute CHUNK_04 Feature Engineering (DATA LEAKAGE FIXED)

    Args:
        cleaned_datasets: Dictionary of cleaned DataFrames from CHUNK_02
        chunk03_results: Analysis results from CHUNK_03 (optional)

    Returns:
        Dictionary with engineered features and metadata
    """

    print("=" * 80)
    print("QUALITY GATE 1: SEPARATE TARGET FROM FEATURES")
    print("=" * 80 + "\n")

    # Store targets separately
    targets_dict = {}
    features_only_dict = {}

    for filename, df in cleaned_datasets.items():
        print(f"Processing: {filename}")

        # Identify target column
        target_candidates = ['TARGET', 'target', 'Target', 'default', 'Default', 'label', 'Label']
        target_col = None

        for col in target_candidates:
            if col in df.columns:
                target_col = col
                break

        if target_col:
            # REMOVE TARGET from features (CRITICAL - prevents data leakage)
            targets_dict[filename] = df[target_col].copy()
            df_features = df.drop(columns=[target_col])
            features_only_dict[filename] = df_features
            print(f"  [OK] Separated TARGET column: '{target_col}'")
            print(f"  Features shape: {df_features.shape} (target removed)\n")
        else:
            # No target in this dataset
            features_only_dict[filename] = df.copy()
            print(f"  [INFO] No target column found\n")

    print("=" * 80)
    print("QUALITY GATE 2: CATEGORICAL ENCODING")
    print("=" * 80 + "\n")

    encoder = CategoricalEncoder()
    encoded_datasets = {}

    for filename, df in features_only_dict.items():
        print(f"Encoding: {filename}")

        categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

        if categorical_cols:
            encoded_df = encoder.label_encode(df, categorical_cols)
            encoded_datasets[filename] = encoded_df
            print(f"  [OK] Encoded {len(categorical_cols)} categorical features\n")
        else:
            encoded_datasets[filename] = df
            print(f"  [INFO] No categorical features\n")

    print("=" * 80)
    print("QUALITY GATE 3: FEATURE SCALING & TRANSFORMATION")
    print("=" * 80 + "\n")

    transformer = FeatureTransformer()
    transformed_datasets = {}

    for filename, df in encoded_datasets.items():
        print(f"Scaling features: {filename}")

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if numeric_cols:
            scaled_df = transformer.standardize(df, numeric_cols)
            transformed_datasets[filename] = scaled_df
            print(f"  [OK] Standardized {len(numeric_cols)} numeric features\n")
        else:
            transformed_datasets[filename] = df
            print(f"  [INFO] No numeric features to scale\n")

    print("=" * 80)
    print("QUALITY GATE 4: FEATURE SELECTION & QUALITY ASSESSMENT")
    print("=" * 80 + "\n")

    assessor = FeatureQualityAssessor()
    selection_results = {}
    quality_assessment = {}

    for filename, df in transformed_datasets.items():
        print(f"Assessing: {filename}")

        # Variance-based selection
        numeric_df = df.select_dtypes(include=[np.number])
        variances = numeric_df.var()
        high_variance_features = variances[variances > 0.01].index.tolist()

        # Redundant features
        redundant = assessor.detect_redundant_features(df, threshold=0.95)

        # Quality assessment
        original_shape = (len(cleaned_datasets[filename]), len(cleaned_datasets[filename].columns))
        quality = assessor.assess_features(df, cleaned_datasets[filename])

        selection_results[filename] = {
            'high_variance_features': high_variance_features,
            'redundant_pairs': redundant
        }

        quality_assessment[filename] = quality

        print(f"  High-variance features: {len(high_variance_features)}")
        print(f"  Redundant pairs: {len(redundant)}")
        print(f"  Features shape: {df.shape}")
        print(f"  Memory increase: {quality['memory_increase_mb']:.2f} MB\n")

    print("=" * 80)
    print("GENERATING SUMMARY REPORT")
    print("=" * 80 + "\n")

    summary = "=" * 80 + "\n"
    summary += "FEATURE ENGINEERING SUMMARY (DATA LEAKAGE FIXED)\n"
    summary += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    summary += "=" * 80 + "\n\n"

    summary += "CRITICAL: TARGET COLUMN REMOVED FROM ALL FEATURES\n"
    summary += "No polynomial or ratio features created with TARGET\n"
    summary += "Data leakage prevented\n\n"

    for filename in transformed_datasets.keys():
        summary += f"\n{filename}\n"
        summary += "-" * 80 + "\n"

        if filename in quality_assessment:
            quality = quality_assessment[filename]
            summary += f"Original Features: {quality['total_original']}\n"
            summary += f"Final Features: {quality['total_new']}\n"
            summary += f"Memory Increase: {quality['memory_increase_mb']:.2f} MB\n"

        if filename in selection_results:
            selection = selection_results[filename]
            summary += f"High-Variance Features: {len(selection['high_variance_features'])}\n"
            summary += f"Redundant Pairs Detected: {len(selection['redundant_pairs'])}\n"

    summary += "\n" + "=" * 80 + "\n"

    print(summary)

    print("\n" + "=" * 80)
    print("CHUNK_04: FEATURE ENGINEERING COMPLETE (DATA LEAKAGE FIXED)")
    print("=" * 80 + "\n")

    print("Ready for CHUNK_05 - Model Selection & Training\n")

    return {
        'engineered_datasets': transformed_datasets,
        'targets_dict': targets_dict,
        'quality_assessment': quality_assessment,
        'selection_results': selection_results,
        'summary': summary
    }


# ============================================================================
# AUTO-RUN IF CHUNK_02 RESULTS AVAILABLE
# ============================================================================

if __name__ == '__main__' or 'chunk02_results' in globals():
    try:
        if 'chunk02_results' in globals():
            print("[OK] Found CHUNK_02 results\n")
            chunk04_results = run_chunk04(cleaned_datasets=chunk02_results['cleaned_datasets'])
        else:
            print("[INFO] CHUNK_02 results not found. Call manually:")
            print("    chunk04_results = run_chunk04(cleaned_datasets=chunk02_results['cleaned_datasets'])")
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        print("\n[INFO] To run manually, use:")
        print("    chunk04_results = run_chunk04(cleaned_datasets=chunk02_results['cleaned_datasets'])")
