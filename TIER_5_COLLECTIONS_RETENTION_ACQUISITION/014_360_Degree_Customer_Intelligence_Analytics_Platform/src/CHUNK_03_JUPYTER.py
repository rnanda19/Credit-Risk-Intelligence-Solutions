#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CHUNK_03: FEATURE VALIDATION & EXPLORATION - JUPYTER VERSION
================================================================================

Simple, step-by-step version for Jupyter notebooks.
Just copy and paste each cell into your Jupyter notebook.

================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

print("\n" + "=" * 80)
print("CHUNK_03: FEATURE VALIDATION & EXPLORATION")
print("=" * 80 + "\n")

# ============================================================================
# CELL 1: QUALITY GATE 1 - FEATURE DISTRIBUTION ANALYSIS
# ============================================================================

print("=" * 80)
print("QUALITY GATE 1: FEATURE DISTRIBUTION ANALYSIS")
print("=" * 80 + "\n")

all_features_analysis = {}

for filename, df in chunk02_results['cleaned_datasets'].items():
    print(f"Analyzing: {filename}")
    print(f"  Shape: {df.shape}")

    features_analysis = {}

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            # Numeric feature
            features_analysis[col] = {
                'type': 'numeric',
                'dtype': str(df[col].dtype),
                'missing_pct': round((df[col].isnull().sum() / len(df)) * 100, 2),
                'unique': int(df[col].nunique()),
                'min': float(df[col].min()),
                'mean': float(df[col].mean()),
                'median': float(df[col].median()),
                'max': float(df[col].max()),
                'std': float(df[col].std()),
                'skewness': float(df[col].skew())
            }
        else:
            # Categorical feature
            value_counts = df[col].value_counts()
            features_analysis[col] = {
                'type': 'categorical',
                'dtype': str(df[col].dtype),
                'missing_pct': round((df[col].isnull().sum() / len(df)) * 100, 2),
                'unique': int(df[col].nunique()),
                'top_value': str(value_counts.index[0]) if len(value_counts) > 0 else 'N/A',
                'top_value_pct': round(value_counts.values[0] / len(df) * 100, 2) if len(value_counts) > 0 else 0
            }

    all_features_analysis[filename] = features_analysis
    print(f"  [OK] Analyzed {len(features_analysis)} features")
    print(f"  Numeric: {len([f for f in features_analysis.values() if f['type'] == 'numeric'])}")
    print(f"  Categorical: {len([f for f in features_analysis.values() if f['type'] == 'categorical'])}\n")

# ============================================================================
# CELL 2: QUALITY GATE 2 - CORRELATION ANALYSIS
# ============================================================================

print("=" * 80)
print("QUALITY GATE 2: CORRELATION ANALYSIS")
print("=" * 80 + "\n")

correlation_results = {}

for filename, df in chunk02_results['cleaned_datasets'].items():
    print(f"Analyzing correlations: {filename}")

    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()

        # Find high correlations
        high_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > 0.8:
                    high_corr.append((
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        round(corr_matrix.iloc[i, j], 4)
                    ))

        correlation_results[filename] = high_corr
        print(f"  [OK] Found {len(high_corr)} highly correlated pairs (>0.8)\n")
    else:
        correlation_results[filename] = []
        print(f"  [INFO] Only {len(numeric_cols)} numeric feature(s)\n")

# ============================================================================
# CELL 3: QUALITY GATE 3 - FEATURE QUALITY ASSESSMENT
# ============================================================================

print("=" * 80)
print("QUALITY GATE 3: FEATURE QUALITY ASSESSMENT")
print("=" * 80 + "\n")

quality_results = {}

for filename, df in chunk02_results['cleaned_datasets'].items():
    print(f"Assessing quality: {filename}")

    quality_scores = {}

    for col in df.columns:
        missing_pct = (df[col].isnull().sum() / len(df)) * 100
        unique_pct = (df[col].nunique() / len(df)) * 100

        completeness = 100 - missing_pct
        variety = min(unique_pct, 100)
        quality_score = (completeness * 0.7 + variety * 0.3)

        quality_scores[col] = round(quality_score, 2)

    quality_results[filename] = quality_scores

    avg_quality = np.mean(list(quality_scores.values()))
    low_quality = len([s for s in quality_scores.values() if s < 50])

    print(f"  Average quality score: {avg_quality:.2f}/100")
    print(f"  Low-quality features: {low_quality}")
    print(f"  [OK] Assessed {len(quality_scores)} features\n")

# ============================================================================
# CELL 4: QUALITY GATE 4 - STATISTICAL VALIDATION
# ============================================================================

print("=" * 80)
print("QUALITY GATE 4: STATISTICAL VALIDATION")
print("=" * 80 + "\n")

statistical_results = {}

for filename, df in chunk02_results['cleaned_datasets'].items():
    print(f"Validating: {filename}")

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns

    stats_summary = {
        'shape': df.shape,
        'numeric_features': len(numeric_cols),
        'categorical_features': len(categorical_cols),
        'memory_mb': round(df.memory_usage(deep=True).sum() / (1024**2), 2),
        'total_missing_pct': round((df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100, 2)
    }

    statistical_results[filename] = stats_summary

    print(f"  Shape: {stats_summary['shape'][0]:,} rows, {stats_summary['shape'][1]} columns")
    print(f"  Memory: {stats_summary['memory_mb']:.2f} MB")
    print(f"  Total missing: {stats_summary['total_missing_pct']:.2f}%\n")

# ============================================================================
# CELL 5: GENERATE SUMMARY
# ============================================================================

print("=" * 80)
print("GENERATING SUMMARY REPORT")
print("=" * 80 + "\n")

summary = "=" * 80 + "\n"
summary += "FEATURE VALIDATION & EXPLORATION SUMMARY\n"
summary += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
summary += "=" * 80 + "\n\n"

for filename in chunk02_results['cleaned_datasets'].keys():
    summary += f"\n{filename}\n"
    summary += "-" * 80 + "\n"

    if filename in statistical_results:
        stats = statistical_results[filename]
        summary += f"Shape: {stats['shape'][0]:,} rows, {stats['shape'][1]} columns\n"
        summary += f"Memory: {stats['memory_mb']:.2f} MB\n"
        summary += f"Numeric Features: {stats['numeric_features']}\n"
        summary += f"Categorical Features: {stats['categorical_features']}\n"
        summary += f"Total Missing: {stats['total_missing_pct']:.2f}%\n"

    if filename in correlation_results:
        summary += f"High-Correlation Pairs: {len(correlation_results[filename])}\n"

    if filename in quality_results:
        avg_quality = np.mean(list(quality_results[filename].values()))
        summary += f"Average Quality Score: {avg_quality:.2f}/100\n"

summary += "\n" + "=" * 80 + "\n"

print(summary)

# ============================================================================
# CELL 6: STORE RESULTS
# ============================================================================

print("=" * 80)
print("CHUNK_03: FEATURE VALIDATION & EXPLORATION COMPLETE")
print("=" * 80 + "\n")

chunk03_results = {
    'features_analysis': all_features_analysis,
    'correlation_results': correlation_results,
    'quality_results': quality_results,
    'statistical_results': statistical_results,
    'summary': summary
}

print("✓ Results stored in 'chunk03_results'")
print("✓ Ready for CHUNK_04 - Feature Engineering\n")

print("Access results with:")
print("  - chunk03_results['features_analysis']")
print("  - chunk03_results['correlation_results']")
print("  - chunk03_results['quality_results']")
print("  - chunk03_results['statistical_results']")
print("  - chunk03_results['summary']")
