#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
CHUNK_03: FEATURE VALIDATION & EXPLORATION - COMPLETE VERSION
================================================================================

Complete standalone version that works in Jupyter notebooks.
No external imports needed beyond pandas and numpy.

USAGE IN JUPYTER:
    %cd "path/to/CHUNK_03_FEATURE_VALIDATION"
    exec(open('scripts/CHUNK_03_COMPLETE.py').read())

Then call:
    chunk03_results = run_chunk03(cleaned_datasets=chunk02_results['cleaned_datasets'])

================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
from scipy import stats

print("\n" + "=" * 80)
print("CHUNK_03: FEATURE VALIDATION & EXPLORATION")
print("=" * 80 + "\n")

# ============================================================================
# UTILITY CLASSES
# ============================================================================

class FeatureDistributionAnalyzer:
    """Analyze feature distributions"""

    def __init__(self):
        pass

    def analyze_numeric_distribution(self, series, name="Feature"):
        """Analyze numeric feature distribution"""
        return {
            'name': name,
            'dtype': str(series.dtype),
            'count': int(series.notna().sum()),
            'missing': int(series.isnull().sum()),
            'missing_pct': round((series.isnull().sum() / len(series)) * 100, 2),
            'unique': int(series.nunique()),
            'min': float(series.min()),
            'q25': float(series.quantile(0.25)),
            'median': float(series.median()),
            'q75': float(series.quantile(0.75)),
            'max': float(series.max()),
            'mean': float(series.mean()),
            'std': float(series.std()),
            'skewness': float(series.skew()),
            'kurtosis': float(series.kurtosis())
        }

    def analyze_categorical_distribution(self, series, name="Feature", top_n=10):
        """Analyze categorical feature distribution"""
        value_counts = series.value_counts()
        return {
            'name': name,
            'dtype': str(series.dtype),
            'count': int(series.notna().sum()),
            'missing': int(series.isnull().sum()),
            'missing_pct': round((series.isnull().sum() / len(series)) * 100, 2),
            'unique': int(series.nunique()),
            'top_values': value_counts.head(top_n).to_dict(),
            'top_values_pct': (value_counts.head(top_n) / len(series) * 100).round(2).to_dict()
        }

    def analyze_all_features(self, df):
        """Analyze all features in DataFrame"""
        features_analysis = {}

        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                features_analysis[col] = self.analyze_numeric_distribution(df[col], col)
            else:
                features_analysis[col] = self.analyze_categorical_distribution(df[col], col)

        print(f"[OK] Analyzed {len(features_analysis)} features")
        return features_analysis


class CorrelationAnalyzer:
    """Analyze feature correlations"""

    def __init__(self):
        pass

    def compute_correlation_matrix(self, df, method='pearson'):
        """Compute correlation matrix"""
        numeric_df = df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr(method=method)
        print(f"[OK] Computed {method} correlation for {len(numeric_df.columns)} features")
        return corr_matrix

    def find_high_correlations(self, corr_matrix, threshold=0.8):
        """Find highly correlated feature pairs"""
        high_corr = []

        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > threshold:
                    high_corr.append((
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        round(corr_matrix.iloc[i, j], 4)
                    ))

        print(f"[OK] Found {len(high_corr)} highly correlated pairs (>{threshold})")
        return high_corr


class FeatureQualityAssessor:
    """Assess feature quality"""

    def __init__(self):
        pass

    def assess_feature_quality(self, df):
        """Assess quality of all features"""
        quality_scores = {}

        for col in df.columns:
            missing_pct = (df[col].isnull().sum() / len(df)) * 100
            unique_pct = (df[col].nunique() / len(df)) * 100

            completeness = 100 - missing_pct
            variety = min(unique_pct, 100)
            quality_score = (completeness * 0.7 + variety * 0.3)

            quality_scores[col] = {
                'completeness': round(completeness, 2),
                'variety': round(variety, 2),
                'quality_score': round(quality_score, 2)
            }

        return quality_scores

    def identify_low_quality_features(self, df, threshold=50.0):
        """Identify low-quality features"""
        quality_scores = self.assess_feature_quality(df)
        low_quality = [col for col, scores in quality_scores.items()
                      if scores['quality_score'] < threshold]

        if low_quality:
            print(f"[WARNING] Found {len(low_quality)} low-quality features (score < {threshold})")

        return low_quality


class StatisticalValidator:
    """Validate features statistically"""

    def __init__(self):
        pass

    def detect_skewness(self, series):
        """Detect feature skewness"""
        skew = series.skew()

        if abs(skew) < 0.5:
            skew_type = 'Approximately Symmetric'
        elif skew > 0:
            skew_type = 'Right Skewed'
        else:
            skew_type = 'Left Skewed'

        return {
            'skewness': round(float(skew), 4),
            'type': skew_type,
            'magnitude': 'Moderate' if 0.5 <= abs(skew) < 1 else ('High' if abs(skew) >= 1 else 'Low')
        }

    def detect_outliers_iqr(self, series):
        """Detect outliers using IQR method"""
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = (series < lower_bound) | (series > upper_bound)
        outlier_count = outliers.sum()
        outlier_pct = (outlier_count / len(series)) * 100

        return {
            'method': 'IQR',
            'outlier_count': int(outlier_count),
            'outlier_pct': round(outlier_pct, 2),
            'has_outliers': outlier_count > 0
        }


# ============================================================================
# MAIN EXECUTION FUNCTION
# ============================================================================

def run_chunk03(cleaned_datasets):
    """
    Execute CHUNK_03 Feature Validation & Exploration

    Args:
        cleaned_datasets: Dictionary of cleaned DataFrames from CHUNK_02

    Returns:
        Dictionary with analysis results
    """

    print("=" * 80)
    print("QUALITY GATE 1: FEATURE DISTRIBUTION ANALYSIS")
    print("=" * 80 + "\n")

    dist_analyzer = FeatureDistributionAnalyzer()
    all_features_analysis = {}

    for filename, df in cleaned_datasets.items():
        print(f"Analyzing: {filename}")
        features_analysis = dist_analyzer.analyze_all_features(df)
        all_features_analysis[filename] = features_analysis

    print("\n" + "=" * 80)
    print("QUALITY GATE 2: CORRELATION ANALYSIS")
    print("=" * 80 + "\n")

    corr_analyzer = CorrelationAnalyzer()
    correlation_results = {}

    for filename, df in cleaned_datasets.items():
        print(f"Analyzing correlations: {filename}")
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) > 1:
            corr_matrix = corr_analyzer.compute_correlation_matrix(df)
            high_corr = corr_analyzer.find_high_correlations(corr_matrix, threshold=0.8)
            correlation_results[filename] = {
                'high_correlations': high_corr,
                'numeric_features': len(numeric_cols)
            }
        else:
            print(f"[INFO] Skipped - only {len(numeric_cols)} numeric feature(s)")
            correlation_results[filename] = {'high_correlations': [], 'numeric_features': len(numeric_cols)}

    print("\n" + "=" * 80)
    print("QUALITY GATE 3: FEATURE QUALITY ASSESSMENT")
    print("=" * 80 + "\n")

    quality_assessor = FeatureQualityAssessor()
    quality_results = {}

    for filename, df in cleaned_datasets.items():
        print(f"Assessing quality: {filename}")
        quality_scores = quality_assessor.assess_feature_quality(df)
        quality_results[filename] = quality_scores

        avg_quality = np.mean([scores['quality_score'] for scores in quality_scores.values()])
        low_quality_count = len([s for s in quality_scores.values() if s['quality_score'] < 50])
        print(f"  Average quality score: {avg_quality:.2f}/100")
        print(f"  Low-quality features: {low_quality_count}")

    print("\n" + "=" * 80)
    print("QUALITY GATE 4: STATISTICAL VALIDATION")
    print("=" * 80 + "\n")

    validator = StatisticalValidator()
    statistical_results = {}

    for filename, df in cleaned_datasets.items():
        print(f"Validating: {filename}")
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        stats_summary = {
            'total_features': len(df.columns),
            'numeric_features': len(numeric_cols),
            'categorical_features': len(df.columns) - len(numeric_cols),
            'shape': df.shape,
            'memory_mb': round(df.memory_usage(deep=True).sum() / (1024**2), 2)
        }

        statistical_results[filename] = stats_summary
        print(f"  Shape: {df.shape}")
        print(f"  Memory: {stats_summary['memory_mb']:.2f} MB")

    print("\n" + "=" * 80)
    print("GENERATING REPORTS")
    print("=" * 80 + "\n")

    # Generate summary report
    summary = "=" * 80 + "\n"
    summary += "FEATURE VALIDATION & EXPLORATION SUMMARY\n"
    summary += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    summary += "=" * 80 + "\n\n"

    for filename in cleaned_datasets.keys():
        summary += f"\n{filename}\n"
        summary += "-" * 80 + "\n"

        if filename in statistical_results:
            stats = statistical_results[filename]
            summary += f"Shape: {stats['shape'][0]:,} rows, {stats['shape'][1]} columns\n"
            summary += f"Memory: {stats['memory_mb']:.2f} MB\n"
            summary += f"Numeric Features: {stats['numeric_features']}\n"
            summary += f"Categorical Features: {stats['categorical_features']}\n"

        if filename in correlation_results:
            corr = correlation_results[filename]
            summary += f"High-Correlation Pairs: {len(corr['high_correlations'])}\n"

        if filename in quality_results:
            quality = quality_results[filename]
            avg_quality = np.mean([s['quality_score'] for s in quality.values()])
            summary += f"Average Quality Score: {avg_quality:.2f}/100\n"

    summary += "\n" + "=" * 80 + "\n"

    print("[OK] Report generated")

    print("\n" + "=" * 80)
    print("CHUNK_03: FEATURE VALIDATION & EXPLORATION COMPLETE")
    print("=" * 80 + "\n")

    print("Ready for CHUNK_04 - Feature Engineering\n")

    return {
        'features_analysis': all_features_analysis,
        'correlation_results': correlation_results,
        'quality_results': quality_results,
        'statistical_results': statistical_results,
        'summary': summary
    }


# ============================================================================
# AUTO-RUN IF CHUNK_02 RESULTS AVAILABLE
# ============================================================================

if __name__ == '__main__' or 'chunk02_results' in globals():
    try:
        if 'chunk02_results' in globals():
            print("[OK] Found CHUNK_02 results\n")
            chunk03_results = run_chunk03(cleaned_datasets=chunk02_results['cleaned_datasets'])
        else:
            print("[INFO] CHUNK_02 results not found. Call manually:")
            print("    chunk03_results = run_chunk03(cleaned_datasets=chunk02_results['cleaned_datasets'])")
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        print("\n[INFO] To run manually, use:")
        print("    chunk03_results = run_chunk03(cleaned_datasets=chunk02_results['cleaned_datasets'])")
