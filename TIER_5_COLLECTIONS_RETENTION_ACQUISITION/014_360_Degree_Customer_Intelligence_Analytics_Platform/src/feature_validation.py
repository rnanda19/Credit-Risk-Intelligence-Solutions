#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
CHUNK_03: FEATURE VALIDATION UTILITY LIBRARY
================================================================================

MODULE: feature_validation.py
PURPOSE: Core utility functions for feature exploration and validation
VERSION: 1.0.0
DATE: August 12, 2026

This module provides reusable functions for:
- Feature distribution analysis
- Statistical validation
- Correlation analysis
- Feature quality assessment
- Missing value patterns
- Outlier detection
- Data exploration reports

================================================================================
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from scipy import stats
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# FEATURE DISTRIBUTION ANALYSIS
# ============================================================================

class FeatureDistributionAnalyzer:
    """Analyze feature distributions"""

    def __init__(self, log_func=None):
        self.log_func = log_func or self._default_log

    def _default_log(self, message: str, level: str = "INFO"):
        print(f"[{level}] {message}")

    def analyze_numeric_distribution(self, series: pd.Series, name: str = "Feature") -> Dict:
        """
        Analyze numeric feature distribution

        Args:
            series: Numeric Series
            name: Feature name

        Returns:
            Dictionary with distribution statistics
        """
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

    def analyze_categorical_distribution(self, series: pd.Series, name: str = "Feature",
                                        top_n: int = 10) -> Dict:
        """
        Analyze categorical feature distribution

        Args:
            series: Categorical Series
            name: Feature name
            top_n: Number of top categories to show

        Returns:
            Dictionary with distribution statistics
        """
        value_counts = series.value_counts()

        return {
            'name': name,
            'dtype': str(series.dtype),
            'count': int(series.notna().sum()),
            'missing': int(series.isnull().sum()),
            'missing_pct': round((series.isnull().sum() / len(series)) * 100, 2),
            'unique': int(series.nunique()),
            'top_values': value_counts.head(top_n).to_dict(),
            'top_values_pct': (value_counts.head(top_n) / len(series) * 100).to_dict()
        }

    def analyze_all_features(self, df: pd.DataFrame) -> Dict:
        """
        Analyze all features in DataFrame

        Args:
            df: DataFrame to analyze

        Returns:
            Dictionary with all feature analyses
        """
        self.log_func(f"\nAnalyzing {len(df.columns)} features...")

        features_analysis = {}

        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                features_analysis[col] = self.analyze_numeric_distribution(df[col], col)
            else:
                features_analysis[col] = self.analyze_categorical_distribution(df[col], col)

        self.log_func(f"[OK] Analyzed {len(features_analysis)} features\n")
        return features_analysis


# ============================================================================
# CORRELATION ANALYSIS
# ============================================================================

class CorrelationAnalyzer:
    """Analyze feature correlations"""

    def __init__(self, log_func=None):
        self.log_func = log_func or self._default_log

    def _default_log(self, message: str, level: str = "INFO"):
        print(f"[{level}] {message}")

    def compute_correlation_matrix(self, df: pd.DataFrame, method: str = 'pearson') -> pd.DataFrame:
        """
        Compute correlation matrix

        Args:
            df: DataFrame with numeric columns
            method: 'pearson', 'spearman', or 'kendall'

        Returns:
            Correlation matrix
        """
        numeric_df = df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr(method=method)
        self.log_func(f"[OK] Computed {method} correlation for {len(numeric_df.columns)} features")
        return corr_matrix

    def find_high_correlations(self, corr_matrix: pd.DataFrame, threshold: float = 0.8) -> List[Tuple]:
        """
        Find highly correlated feature pairs

        Args:
            corr_matrix: Correlation matrix
            threshold: Correlation threshold (default 0.8)

        Returns:
            List of (feature1, feature2, correlation) tuples
        """
        high_corr = []

        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > threshold:
                    high_corr.append((
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        corr_matrix.iloc[i, j]
                    ))

        self.log_func(f"[OK] Found {len(high_corr)} highly correlated pairs (>{threshold})")
        return high_corr

    def analyze_feature_correlations(self, df: pd.DataFrame, target: str = None) -> Dict:
        """
        Analyze feature correlations

        Args:
            df: DataFrame
            target: Target column name (if exists)

        Returns:
            Dictionary with correlation analysis
        """
        corr_matrix = self.compute_correlation_matrix(df)
        high_corr_pairs = self.find_high_correlations(corr_matrix, threshold=0.8)

        result = {
            'correlation_matrix': corr_matrix.to_dict(),
            'high_correlations': high_corr_pairs,
            'n_features': len(corr_matrix.columns)
        }

        if target and target in corr_matrix.columns:
            result['target_correlations'] = corr_matrix[target].sort_values(ascending=False).to_dict()

        return result


# ============================================================================
# FEATURE QUALITY ASSESSMENT
# ============================================================================

class FeatureQualityAssessor:
    """Assess feature quality"""

    def __init__(self, log_func=None):
        self.log_func = log_func or self._default_log

    def _default_log(self, message: str, level: str = "INFO"):
        print(f"[{level}] {message}")

    def assess_feature_quality(self, df: pd.DataFrame) -> Dict:
        """
        Assess quality of all features

        Args:
            df: DataFrame to assess

        Returns:
            Dictionary with quality scores
        """
        quality_scores = {}

        for col in df.columns:
            missing_pct = (df[col].isnull().sum() / len(df)) * 100

            if pd.api.types.is_numeric_dtype(df[col]):
                unique_pct = (df[col].nunique() / len(df)) * 100
            else:
                unique_pct = (df[col].nunique() / len(df)) * 100

            # Quality score (0-100)
            completeness = 100 - missing_pct
            variety = min(unique_pct, 100)
            quality_score = (completeness * 0.7 + variety * 0.3)

            quality_scores[col] = {
                'completeness': round(completeness, 2),
                'variety': round(variety, 2),
                'quality_score': round(quality_score, 2)
            }

        self.log_func(f"[OK] Assessed quality for {len(quality_scores)} features")
        return quality_scores

    def identify_low_quality_features(self, df: pd.DataFrame, threshold: float = 50.0) -> List[str]:
        """
        Identify low-quality features

        Args:
            df: DataFrame
            threshold: Quality score threshold (default 50)

        Returns:
            List of low-quality feature names
        """
        quality_scores = self.assess_feature_quality(df)
        low_quality = [col for col, scores in quality_scores.items()
                       if scores['quality_score'] < threshold]

        if low_quality:
            self.log_func(f"[WARNING] Found {len(low_quality)} low-quality features (score < {threshold})")
            self.log_func(f"Features: {low_quality}")

        return low_quality


# ============================================================================
# STATISTICAL VALIDATION
# ============================================================================

class StatisticalValidator:
    """Validate features statistically"""

    def __init__(self, log_func=None):
        self.log_func = log_func or self._default_log

    def _default_log(self, message: str, level: str = "INFO"):
        print(f"[{level}] {message}")

    def test_normality(self, series: pd.Series, method: str = 'shapiro') -> Dict:
        """
        Test feature normality

        Args:
            series: Numeric Series
            method: 'shapiro' or 'anderson'

        Returns:
            Dictionary with test results
        """
        series_clean = series.dropna()

        if method == 'shapiro':
            stat, p_value = stats.shapiro(series_clean[:5000])  # Limit to 5000 for performance
            return {
                'test': 'Shapiro-Wilk',
                'statistic': float(stat),
                'p_value': float(p_value),
                'normal': p_value > 0.05
            }
        else:
            result = stats.anderson(series_clean)
            return {
                'test': 'Anderson-Darling',
                'statistic': float(result.statistic),
                'critical_values': list(result.critical_values),
                'significance_levels': list(result.significance_level)
            }

    def detect_skewness(self, series: pd.Series) -> Dict:
        """
        Detect feature skewness

        Args:
            series: Numeric Series

        Returns:
            Dictionary with skewness analysis
        """
        skew = series.skew()

        if abs(skew) < 0.5:
            skew_type = 'Approximately Symmetric'
        elif skew > 0:
            skew_type = 'Right Skewed'
        else:
            skew_type = 'Left Skewed'

        return {
            'skewness': float(skew),
            'type': skew_type,
            'magnitude': 'Moderate' if 0.5 <= abs(skew) < 1 else ('High' if abs(skew) >= 1 else 'Low')
        }

    def detect_outliers_statistical(self, series: pd.Series, method: str = 'zscore',
                                    threshold: float = 3.0) -> Dict:
        """
        Detect outliers using statistical methods

        Args:
            series: Numeric Series
            method: 'zscore' or 'iqr'
            threshold: Threshold for z-score (default 3.0)

        Returns:
            Dictionary with outlier detection results
        """
        series_clean = series.dropna()

        if method == 'zscore':
            z_scores = np.abs(stats.zscore(series_clean))
            outliers = z_scores > threshold
            outlier_count = outliers.sum()
            outlier_pct = (outlier_count / len(series_clean)) * 100
        else:  # IQR
            Q1 = series_clean.quantile(0.25)
            Q3 = series_clean.quantile(0.75)
            IQR = Q3 - Q1
            outliers = (series_clean < Q1 - 1.5*IQR) | (series_clean > Q3 + 1.5*IQR)
            outlier_count = outliers.sum()
            outlier_pct = (outlier_count / len(series_clean)) * 100

        return {
            'method': method,
            'outlier_count': int(outlier_count),
            'outlier_pct': round(outlier_pct, 2),
            'has_outliers': outlier_count > 0
        }


# ============================================================================
# EXPLORATION REPORT GENERATOR
# ============================================================================

class ExplorationReportGenerator:
    """Generate feature exploration reports"""

    def __init__(self, log_func=None):
        self.log_func = log_func or self._default_log

    def _default_log(self, message: str, level: str = "INFO"):
        print(f"[{level}] {message}")

    def generate_feature_report(self, df: pd.DataFrame, features_analysis: Dict) -> str:
        """
        Generate feature exploration report

        Args:
            df: DataFrame
            features_analysis: Dictionary with feature analyses

        Returns:
            Formatted report string
        """
        report = "=" * 80 + "\n"
        report += "FEATURE EXPLORATION REPORT\n"
        report += "=" * 80 + "\n\n"

        report += f"Total Features: {len(df.columns)}\n"
        report += f"Total Records: {len(df):,}\n"
        report += f"Total Memory: {df.memory_usage(deep=True).sum() / (1024**2):.2f} MB\n\n"

        numeric_features = df.select_dtypes(include=[np.number]).columns
        categorical_features = df.select_dtypes(exclude=[np.number]).columns

        report += f"Numeric Features: {len(numeric_features)}\n"
        report += f"Categorical Features: {len(categorical_features)}\n\n"

        report += "-" * 80 + "\n"
        report += "TOP NUMERIC FEATURES (by variance)\n"
        report += "-" * 80 + "\n"

        for col in numeric_features[:10]:
            if col in features_analysis:
                analysis = features_analysis[col]
                report += f"\n{col}\n"
                report += f"  Data Type: {analysis['dtype']}\n"
                report += f"  Missing: {analysis['missing_pct']}%\n"
                report += f"  Range: [{analysis['min']:.2f}, {analysis['max']:.2f}]\n"
                report += f"  Mean: {analysis['mean']:.2f} (+/- {analysis['std']:.2f})\n"
                report += f"  Skewness: {analysis['skewness']:.2f}\n"

        report += "\n" + "-" * 80 + "\n"
        report += "TOP CATEGORICAL FEATURES\n"
        report += "-" * 80 + "\n"

        for col in categorical_features[:10]:
            if col in features_analysis:
                analysis = features_analysis[col]
                report += f"\n{col}\n"
                report += f"  Unique Values: {analysis['unique']}\n"
                report += f"  Missing: {analysis['missing_pct']}%\n"
                report += f"  Top Value: {list(analysis['top_values'].keys())[0]}\n"

        report += "\n" + "=" * 80 + "\n"
        return report


if __name__ == "__main__":
    print("Feature Validation Library - CHUNK_03")
    print("Classes available:")
    print("  - FeatureDistributionAnalyzer")
    print("  - CorrelationAnalyzer")
    print("  - FeatureQualityAssessor")
    print("  - StatisticalValidator")
    print("  - ExplorationReportGenerator")
