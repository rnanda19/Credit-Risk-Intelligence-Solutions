#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
CHUNK_03: FEATURE VALIDATION & EXPLORATION (INTERACTIVE VERSION)
================================================================================

This version is optimized for Jupyter notebooks and interactive environments.

Usage in Jupyter:
    # Load cleaned data from CHUNK_02 first
    chunk02_results = run_chunk02(datasets=results['datasets'])
    cleaned_datasets = chunk02_results['cleaned_datasets']

    # Then run:
    exec(open('CHUNK_03_INTERACTIVE.py').read())
"""

import os
import sys
import json
import logging
import platform
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

print("\n" + "=" * 80)
print("CHUNK_03: FEATURE VALIDATION & EXPLORATION (INTERACTIVE)")
print("=" * 80 + "\n")

# ============================================================================
# PATH SETUP
# ============================================================================

def get_chunk03_directory():
    """Find CHUNK_03_FEATURE_VALIDATION directory"""
    cwd = os.getcwd()

    if "CHUNK_03_FEATURE_VALIDATION" in cwd:
        return cwd
    if os.path.exists("CHUNK_03_FEATURE_VALIDATION"):
        return os.path.abspath("CHUNK_03_FEATURE_VALIDATION")
    if os.path.exists(os.path.join("..", "CHUNK_03_FEATURE_VALIDATION")):
        return os.path.abspath("../CHUNK_03_FEATURE_VALIDATION")

    windows_path = r"C:\Users\rnand\Documents\home-credit-default-risk\Enterprise_AI_Workflows\PROBLEM_004_Customer_360_Analysis\CHUNK_03_FEATURE_VALIDATION"
    if os.path.exists(windows_path):
        return windows_path

    return cwd

CHUNK_03_DIR = get_chunk03_directory()
LIB_DIR = os.path.join(CHUNK_03_DIR, "lib")
CONFIG_DIR = os.path.join(CHUNK_03_DIR, "config")
DOCS_DIR = os.path.join(CHUNK_03_DIR, "documentation")
LOGS_DIR = os.path.join(CHUNK_03_DIR, "logs")

for directory in [CONFIG_DIR, DOCS_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

print(f"[OK] CHUNK_03 Directory: {CHUNK_03_DIR}\n")

# ============================================================================
# IMPORT VALIDATION LIBRARY
# ============================================================================

sys.path.insert(0, LIB_DIR)

try:
    from feature_validation import (
        FeatureDistributionAnalyzer, CorrelationAnalyzer,
        FeatureQualityAssessor, StatisticalValidator,
        ExplorationReportGenerator
    )
    print("[OK] Imported feature_validation library\n")
except ImportError:
    print("[WARNING] Could not import feature_validation")
    print("[INFO] Creating inline versions...\n")

    # Fallback: Simple inline versions
    class FeatureDistributionAnalyzer:
        def __init__(self, log_func=None):
            self.log_func = log_func or print

        def analyze_numeric_distribution(self, series, name="Feature"):
            return {
                'name': name,
                'dtype': str(series.dtype),
                'count': int(series.notna().sum()),
                'missing_pct': round((series.isnull().sum() / len(series)) * 100, 2),
                'unique': int(series.nunique()),
                'min': float(series.min()),
                'max': float(series.max()),
                'mean': float(series.mean()),
                'median': float(series.median()),
                'std': float(series.std())
            }

        def analyze_all_features(self, df):
            features = {}
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    features[col] = self.analyze_numeric_distribution(df[col], col)
            self.log_func(f"[OK] Analyzed {len(features)} features")
            return features

    class CorrelationAnalyzer:
        def __init__(self, log_func=None):
            self.log_func = log_func or print

        def compute_correlation_matrix(self, df, method='pearson'):
            numeric_df = df.select_dtypes(include=[np.number])
            return numeric_df.corr(method=method)

        def find_high_correlations(self, corr_matrix, threshold=0.8):
            high_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i + 1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > threshold:
                        high_corr.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))
            self.log_func(f"[OK] Found {len(high_corr)} highly correlated pairs")
            return high_corr

    class FeatureQualityAssessor:
        def __init__(self, log_func=None):
            self.log_func = log_func or print

        def assess_feature_quality(self, df):
            quality_scores = {}
            for col in df.columns:
                missing_pct = (df[col].isnull().sum() / len(df)) * 100
                completeness = 100 - missing_pct
                quality_scores[col] = {'completeness': completeness}
            return quality_scores

# ============================================================================
# FEATURE VALIDATION EXECUTION
# ============================================================================

def validate_features(cleaned_datasets):
    """
    Validate and explore features

    Args:
        cleaned_datasets: Dictionary of cleaned DataFrames

    Returns:
        Dictionary with validation results
    """

    print("=" * 80)
    print("QUALITY GATE 1: FEATURE DISTRIBUTION ANALYSIS")
    print("=" * 80 + "\n")

    dist_analyzer = FeatureDistributionAnalyzer()
    all_features_analysis = {}

    for filename, df in cleaned_datasets.items():
        print(f"\nAnalyzing: {filename}")
        features_analysis = dist_analyzer.analyze_all_features(df)
        all_features_analysis[filename] = features_analysis
        print(f"  Numeric features: {len([f for f in features_analysis.values() if 'q25' in f])}")

    print("\n" + "=" * 80)
    print("QUALITY GATE 2: CORRELATION ANALYSIS")
    print("=" * 80 + "\n")

    corr_analyzer = CorrelationAnalyzer()
    correlation_results = {}

    for filename, df in cleaned_datasets.items():
        print(f"\nAnalyzing correlations: {filename}")
        corr_matrix = corr_analyzer.compute_correlation_matrix(df)
        high_corr = corr_analyzer.find_high_correlations(corr_matrix, threshold=0.8)
        correlation_results[filename] = {
            'high_correlations': high_corr,
            'matrix_shape': corr_matrix.shape
        }

    print("\n" + "=" * 80)
    print("QUALITY GATE 3: FEATURE QUALITY ASSESSMENT")
    print("=" * 80 + "\n")

    quality_assessor = FeatureQualityAssessor()
    quality_results = {}

    for filename, df in cleaned_datasets.items():
        print(f"\nAssessing quality: {filename}")
        quality_scores = quality_assessor.assess_feature_quality(df)
        quality_results[filename] = quality_scores

        # Summary stats
        avg_quality = np.mean([scores.get('quality_score', scores.get('completeness', 0))
                               for scores in quality_scores.values()])
        print(f"  Average quality score: {avg_quality:.2f}/100")

    print("\n" + "=" * 80)
    print("QUALITY GATE 4: STATISTICAL VALIDATION")
    print("=" * 80 + "\n")

    validator = StatisticalValidator()
    statistical_results = {}

    for filename, df in cleaned_datasets.items():
        print(f"\nValidating: {filename}")
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        stats_summary = {
            'total_features': len(df.columns),
            'numeric_features': len(numeric_cols),
            'categorical_features': len(df.columns) - len(numeric_cols)
        }

        statistical_results[filename] = stats_summary
        print(f"  Numeric features: {len(numeric_cols)}")
        print(f"  Categorical features: {len(df.columns) - len(numeric_cols)}")

    return all_features_analysis, correlation_results, quality_results, statistical_results


def generate_exploration_summary(cleaned_datasets, features_analysis):
    """Generate feature exploration summary"""

    print("\n" + "=" * 80)
    print("GENERATING EXPLORATION REPORTS")
    print("=" * 80 + "\n")

    summary = "=" * 80 + "\n"
    summary += "FEATURE VALIDATION & EXPLORATION SUMMARY\n"
    summary += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    summary += "=" * 80 + "\n\n"

    for filename, df in cleaned_datasets.items():
        if filename not in features_analysis:
            continue

        summary += f"\n{filename}\n"
        summary += "-" * 80 + "\n"
        summary += f"Shape: {df.shape[0]:,} rows, {df.shape[1]} columns\n"
        summary += f"Memory: {df.memory_usage(deep=True).sum() / (1024**2):.2f} MB\n"

        numeric_cols = df.select_dtypes(include=[np.number]).columns
        summary += f"Numeric Features: {len(numeric_cols)}\n"
        summary += f"Categorical Features: {len(df.columns) - len(numeric_cols)}\n"

    summary += "\n" + "=" * 80 + "\n"
    return summary


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_chunk03(cleaned_datasets=None):
    """
    Execute CHUNK_03

    Args:
        cleaned_datasets: Dictionary of cleaned DataFrames from CHUNK_02
                         If None, tries to load from CHUNK_02 results
    """

    # Try to get datasets from CHUNK_02 results
    if cleaned_datasets is None:
        try:
            if 'chunk02_results' in globals():
                cleaned_datasets = chunk02_results['cleaned_datasets']
                print("[OK] Using cleaned datasets from CHUNK_02 results\n")
            else:
                print("[ERROR] No datasets provided. Run CHUNK_02 first.")
                return None
        except:
            print("[ERROR] Could not access CHUNK_02 results")
            return None

    # Run validation pipeline
    features_analysis, correlation_results, quality_results, statistical_results = validate_features(cleaned_datasets)

    # Generate reports
    summary = generate_exploration_summary(cleaned_datasets, features_analysis)

    # Save results
    summary_path = os.path.join(DOCS_DIR, 'CHUNK_03_EXPLORATION_SUMMARY.txt')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f"\n[OK] Saved summary: {summary_path}")

    # Save metadata
    metadata = {
        'generated_at': datetime.now().isoformat(),
        'datasets': {},
        'correlations': {},
        'quality': {}
    }

    for filename in cleaned_datasets.keys():
        metadata['datasets'][filename] = {
            'features_analyzed': len(features_analysis.get(filename, {}))
        }
        if filename in correlation_results:
            metadata['correlations'][filename] = {
                'high_correlation_pairs': len(correlation_results[filename]['high_correlations'])
            }
        if filename in quality_results:
            metadata['quality'][filename] = {
                'features_assessed': len(quality_results[filename])
            }

    metadata_path = os.path.join(CONFIG_DIR, 'chunk_03_metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"[OK] Saved metadata: {metadata_path}\n")

    print("=" * 80)
    print("CHUNK_03: FEATURE VALIDATION & EXPLORATION COMPLETE")
    print("=" * 80 + "\n")

    print("Ready for CHUNK_04 - Feature Engineering\n")

    return {
        'features_analysis': features_analysis,
        'correlation_results': correlation_results,
        'quality_results': quality_results,
        'statistical_results': statistical_results,
        'summary': summary
    }


# ============================================================================
# AUTO-RUN IN INTERACTIVE MODE
# ============================================================================

if __name__ == "__main__":
    try:
        if 'chunk02_results' in globals():
            chunk03_results = run_chunk03(cleaned_datasets=chunk02_results['cleaned_datasets'])
        else:
            print("[INFO] No datasets available. Please run CHUNK_02 first.")
    except NameError:
        print("[INFO] Running in script mode. Please provide datasets.")
else:
    try:
        chunk03_results = run_chunk03()
    except:
        print("[INFO] Run with datasets from CHUNK_02:\n")
        print("    chunk03_results = run_chunk03(cleaned_datasets=chunk02_results['cleaned_datasets'])\n")
