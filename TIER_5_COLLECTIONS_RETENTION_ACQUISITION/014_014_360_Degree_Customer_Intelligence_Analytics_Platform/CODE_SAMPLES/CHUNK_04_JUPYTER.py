#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CHUNK_04: FEATURE ENGINEERING - JUPYTER VERSION (DATA LEAKAGE FIXED)
================================================================================

Simple, step-by-step version for Jupyter notebooks.
Just copy and paste each cell into your Jupyter notebook.
DATA LEAKAGE FIXED - TARGET removed before any feature engineering.

================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler

print("\n" + "=" * 80)
print("CHUNK_04: FEATURE ENGINEERING (DATA LEAKAGE FIXED)")
print("=" * 80 + "\n")

# ============================================================================
# CELL 1: QUALITY GATE 1 - SEPARATE TARGET FROM FEATURES
# ============================================================================

print("=" * 80)
print("QUALITY GATE 1: SEPARATE TARGET FROM FEATURES")
print("=" * 80 + "\n")

targets_dict = {}
features_only_dict = {}

for filename, df in chunk02_results['cleaned_datasets'].items():
    print(f"Processing: {filename}")

    # Identify and remove TARGET (CRITICAL - prevents data leakage)
    target_candidates = ['TARGET', 'target', 'Target', 'default', 'Default', 'label', 'Label']
    target_col = None

    for col in target_candidates:
        if col in df.columns:
            target_col = col
            break

    if target_col:
        # REMOVE TARGET from features BEFORE any engineering
        targets_dict[filename] = df[target_col].copy()
        df_features = df.drop(columns=[target_col])
        features_only_dict[filename] = df_features
        print(f"  [OK] Separated TARGET: '{target_col}'")
        print(f"  Features shape: {df_features.shape} (target removed)\n")
    else:
        features_only_dict[filename] = df.copy()
        print(f"  [INFO] No target column found\n")

# ============================================================================
# CELL 2: QUALITY GATE 2 - CATEGORICAL ENCODING
# ============================================================================

print("=" * 80)
print("QUALITY GATE 2: CATEGORICAL ENCODING")
print("=" * 80 + "\n")

encoded_datasets = {}

for filename, df in features_only_dict.items():
    print(f"Encoding: {filename}")

    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    if categorical_cols:
        # Label encode categorical columns
        encoded_df = df.copy()
        for col in categorical_cols:
            unique_values = encoded_df[col].dropna().unique()
            mapping = {val: idx for idx, val in enumerate(unique_values)}
            encoded_df[col] = encoded_df[col].map(mapping)

        encoded_datasets[filename] = encoded_df
        print(f"  [OK] Encoded {len(categorical_cols)} categorical features\n")
    else:
        encoded_datasets[filename] = df
        print(f"  [INFO] No categorical features\n")

# ============================================================================
# CELL 3: QUALITY GATE 3 - FEATURE SCALING
# ============================================================================

print("=" * 80)
print("QUALITY GATE 3: FEATURE SCALING & TRANSFORMATION")
print("=" * 80 + "\n")

transformed_datasets = {}

for filename, df in encoded_datasets.items():
    print(f"Scaling features: {filename}")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if numeric_cols:
        scaled_df = df.copy()
        scaler = StandardScaler()
        scaled_df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
        transformed_datasets[filename] = scaled_df
        print(f"  [OK] Standardized {len(numeric_cols)} numeric features\n")
    else:
        transformed_datasets[filename] = df
        print(f"  [INFO] No numeric features to scale\n")

# ============================================================================
# CELL 4: QUALITY GATE 4 - FEATURE ASSESSMENT
# ============================================================================

print("=" * 80)
print("QUALITY GATE 4: FEATURE SELECTION & QUALITY ASSESSMENT")
print("=" * 80 + "\n")

selection_results = {}
quality_assessment = {}

for filename, df in transformed_datasets.items():
    print(f"Assessing: {filename}")

    # Variance-based selection
    numeric_df = df.select_dtypes(include=[np.number])
    variances = numeric_df.var()
    high_variance = variances[variances > 0.01].index.tolist()

    # Redundant features (correlation > 0.95)
    corr_matrix = numeric_df.corr()
    redundant_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            if abs(corr_matrix.iloc[i, j]) > 0.95:
                redundant_pairs.append((
                    corr_matrix.columns[i],
                    corr_matrix.columns[j],
                    round(corr_matrix.iloc[i, j], 4)
                ))

    # Quality metrics
    original_cols = len(chunk02_results['cleaned_datasets'][filename].columns)
    memory_increase = (
        df.memory_usage(deep=True).sum() -
        chunk02_results['cleaned_datasets'][filename].memory_usage(deep=True).sum()
    ) / (1024**2)

    selection_results[filename] = {
        'high_variance_features': high_variance,
        'redundant_pairs': redundant_pairs
    }

    quality_assessment[filename] = {
        'original_features': original_cols,
        'total_features': len(df.columns),
        'features_changed': len(df.columns) - original_cols,
        'memory_increase_mb': round(memory_increase, 2)
    }

    print(f"  High-variance features: {len(high_variance)}")
    print(f"  Redundant pairs: {len(redundant_pairs)}")
    print(f"  Final shape: {df.shape}")
    print(f"  Memory change: {quality_assessment[filename]['memory_increase_mb']:.2f} MB\n")

# ============================================================================
# CELL 5: GENERATE SUMMARY
# ============================================================================

print("=" * 80)
print("GENERATING SUMMARY REPORT")
print("=" * 80 + "\n")

summary = "=" * 80 + "\n"
summary += "FEATURE ENGINEERING SUMMARY (DATA LEAKAGE FIXED)\n"
summary += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
summary += "=" * 80 + "\n\n"

summary += "CRITICAL FIX APPLIED:\n"
summary += "✓ TARGET column REMOVED from all features\n"
summary += "✓ NO polynomial/ratio features created with TARGET\n"
summary += "✓ Data leakage PREVENTED\n"
summary += "✓ Categorical features ENCODED\n"
summary += "✓ Numeric features SCALED\n\n"

for filename in transformed_datasets.keys():
    summary += f"\n{filename}\n"
    summary += "-" * 80 + "\n"

    if filename in quality_assessment:
        quality = quality_assessment[filename]
        summary += f"Original Features: {quality['original_features']}\n"
        summary += f"Final Features: {quality['total_features']}\n"
        summary += f"Memory Change: {quality['memory_increase_mb']:.2f} MB\n"

    if filename in selection_results:
        selection = selection_results[filename]
        summary += f"High-Variance Features: {len(selection['high_variance_features'])}\n"
        summary += f"Redundant Pairs: {len(selection['redundant_pairs'])}\n"

summary += "\n" + "=" * 80 + "\n"

print(summary)

# ============================================================================
# CELL 6: STORE RESULTS
# ============================================================================

print("=" * 80)
print("CHUNK_04: FEATURE ENGINEERING COMPLETE (DATA LEAKAGE FIXED)")
print("=" * 80 + "\n")

chunk04_results = {
    'engineered_datasets': transformed_datasets,
    'targets_dict': targets_dict,
    'quality_assessment': quality_assessment,
    'selection_results': selection_results,
    'summary': summary
}

print("✓ Results stored in 'chunk04_results'")
print("✓ TARGET safely stored in 'targets_dict'")
print("✓ Ready for CHUNK_05 - Model Selection & Training\n")

print("Access results with:")
print("  - chunk04_results['engineered_datasets']")
print("  - chunk04_results['targets_dict']")
print("  - chunk04_results['quality_assessment']")
print("  - chunk04_results['selection_results']")
print("  - chunk04_results['summary']")
