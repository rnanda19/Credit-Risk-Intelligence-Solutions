#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
CHUNK_02: DATA CLEANING UTILITY LIBRARY
================================================================================

MODULE: data_cleaning.py
PURPOSE: Core utility functions for data cleaning and preprocessing
VERSION: 1.0.0
DATE: August 12, 2026

This module provides reusable functions for:
- Missing value handling
- Duplicate removal
- Outlier detection and treatment
- Data type conversions
- Categorical encoding
- Numerical scaling
- Data quality validation post-cleaning

================================================================================
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# MISSING VALUE HANDLING
# ============================================================================

class MissingValueHandler:
    """Handle missing values in datasets"""

    def __init__(self, log_func=None):
        self.log_func = log_func or self._default_log
        self.missing_stats = {}

    def _default_log(self, message: str, level: str = "INFO"):
        print(f"[{level}] {message}")

    def analyze_missing(self, df: pd.DataFrame) -> Dict:
        """
        Analyze missing values by column

        Args:
            df: DataFrame to analyze

        Returns:
            Dictionary with missing value statistics
        """
        missing_counts = df.isnull().sum()
        missing_pct = (missing_counts / len(df)) * 100

        analysis = {
            'total_missing': int(missing_counts.sum()),
            'total_missing_pct': round((missing_counts.sum() / (df.shape[0] * df.shape[1])) * 100, 2),
            'by_column': missing_counts[missing_counts > 0].to_dict(),
            'by_column_pct': missing_pct[missing_pct > 0].to_dict()
        }

        return analysis

    def drop_high_missing_columns(self, df: pd.DataFrame, threshold: float = 50.0) -> pd.DataFrame:
        """
        Drop columns with high missing value percentage

        Args:
            df: Input DataFrame
            threshold: Missing % threshold (default 50%)

        Returns:
            DataFrame with high-missing columns removed
        """
        initial_cols = len(df.columns)
        missing_pct = (df.isnull().sum() / len(df)) * 100
        cols_to_drop = missing_pct[missing_pct > threshold].index.tolist()

        if cols_to_drop:
            df = df.drop(columns=cols_to_drop)
            self.log_func(f"Dropped {len(cols_to_drop)} columns with >{threshold}% missing")
            self.log_func(f"Columns: {cols_to_drop}")

        return df

    def fill_missing_numeric(self, df: pd.DataFrame, method: str = 'median') -> pd.DataFrame:
        """
        Fill missing numeric values

        Args:
            df: DataFrame with numeric columns
            method: 'mean', 'median', or 'zero'

        Returns:
            DataFrame with filled values
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                if method == 'mean':
                    fill_value = df[col].mean()
                elif method == 'median':
                    fill_value = df[col].median()
                else:  # zero
                    fill_value = 0

                df[col].fillna(fill_value, inplace=True)
                self.log_func(f"Filled {col} with {method}: {fill_value:.2f}")

        return df

    def fill_missing_categorical(self, df: pd.DataFrame, method: str = 'mode') -> pd.DataFrame:
        """
        Fill missing categorical values

        Args:
            df: DataFrame with categorical columns
            method: 'mode' or 'unknown'

        Returns:
            DataFrame with filled values
        """
        categorical_cols = df.select_dtypes(include=['object']).columns

        for col in categorical_cols:
            if df[col].isnull().sum() > 0:
                if method == 'mode':
                    fill_value = df[col].mode()[0] if len(df[col].mode()) > 0 else 'unknown'
                else:
                    fill_value = 'MISSING'

                df[col].fillna(fill_value, inplace=True)
                self.log_func(f"Filled {col} with {method}: {fill_value}")

        return df


# ============================================================================
# DUPLICATE HANDLING
# ============================================================================

class DuplicateHandler:
    """Handle duplicate records"""

    def __init__(self, log_func=None):
        self.log_func = log_func or self._default_log

    def _default_log(self, message: str, level: str = "INFO"):
        print(f"[{level}] {message}")

    def identify_duplicates(self, df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
        """
        Identify duplicate rows

        Args:
            df: DataFrame to check
            subset: Column names to check (None = all columns)

        Returns:
            DataFrame containing duplicate rows
        """
        duplicates = df.duplicated(subset=subset, keep=False)
        dup_df = df[duplicates].sort_values(by=list(df.columns))

        self.log_func(f"Found {dup_df.shape[0]} duplicate records")
        return dup_df

    def remove_duplicates(self, df: pd.DataFrame, subset: List[str] = None,
                         keep: str = 'first') -> pd.DataFrame:
        """
        Remove duplicate rows

        Args:
            df: DataFrame to clean
            subset: Column names to check (None = all columns)
            keep: 'first', 'last', or False (remove all)

        Returns:
            DataFrame with duplicates removed
        """
        initial_rows = len(df)
        df = df.drop_duplicates(subset=subset, keep=keep)
        removed = initial_rows - len(df)

        if removed > 0:
            self.log_func(f"Removed {removed} duplicate rows ({(removed/initial_rows)*100:.2f}%)")

        return df


# ============================================================================
# OUTLIER DETECTION AND HANDLING
# ============================================================================

class OutlierHandler:
    """Detect and handle outliers"""

    def __init__(self, log_func=None):
        self.log_func = log_func or self._default_log

    def _default_log(self, message: str, level: str = "INFO"):
        print(f"[{level}] {message}")

    def detect_iqr_outliers(self, df: pd.DataFrame, column: str,
                           multiplier: float = 1.5) -> pd.Series:
        """
        Detect outliers using IQR method

        Args:
            df: DataFrame
            column: Column name
            multiplier: IQR multiplier (default 1.5)

        Returns:
            Boolean Series marking outliers
        """
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR

        outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
        outlier_count = outliers.sum()

        self.log_func(f"Outliers in {column}: {outlier_count} ({(outlier_count/len(df))*100:.2f}%)")
        return outliers

    def cap_outliers(self, df: pd.DataFrame, column: str, multiplier: float = 1.5) -> pd.DataFrame:
        """
        Cap outliers using IQR method

        Args:
            df: DataFrame
            column: Column name
            multiplier: IQR multiplier

        Returns:
            DataFrame with capped values
        """
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR

        df[column] = df[column].clip(lower=lower_bound, upper=upper_bound)
        self.log_func(f"Capped outliers in {column}")

        return df


# ============================================================================
# DATA TYPE CONVERSION
# ============================================================================

class DataTypeConverter:
    """Convert and optimize data types"""

    def __init__(self, log_func=None):
        self.log_func = log_func or self._default_log

    def _default_log(self, message: str, level: str = "INFO"):
        print(f"[{level}] {message}")

    def optimize_numeric_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize numeric column data types

        Args:
            df: DataFrame to optimize

        Returns:
            DataFrame with optimized numeric types
        """
        original_memory = df.memory_usage(deep=True).sum() / (1024**2)

        for col in df.select_dtypes(include=[np.number]).columns:
            col_type = df[col].dtype

            if col_type == 'int64':
                if df[col].min() >= -128 and df[col].max() <= 127:
                    df[col] = df[col].astype('int8')
                elif df[col].min() >= -32768 and df[col].max() <= 32767:
                    df[col] = df[col].astype('int16')
                elif df[col].min() >= -2147483648 and df[col].max() <= 2147483647:
                    df[col] = df[col].astype('int32')

            elif col_type == 'float64':
                df[col] = df[col].astype('float32')

        optimized_memory = df.memory_usage(deep=True).sum() / (1024**2)
        reduction = ((original_memory - optimized_memory) / original_memory) * 100

        self.log_func(f"Memory: {original_memory:.2f}MB -> {optimized_memory:.2f}MB ({reduction:.1f}% reduction)")

        return df

    def convert_object_to_category(self, df: pd.DataFrame, max_unique: int = 50) -> pd.DataFrame:
        """
        Convert object columns with few unique values to category

        Args:
            df: DataFrame
            max_unique: Maximum unique values for conversion

        Returns:
            DataFrame with optimized categories
        """
        for col in df.select_dtypes(include=['object']).columns:
            unique_count = df[col].nunique()

            if unique_count < max_unique:
                df[col] = df[col].astype('category')
                self.log_func(f"Converted {col} to category ({unique_count} unique values)")

        return df


# ============================================================================
# CATEGORICAL ENCODING
# ============================================================================

class CategoricalEncoder:
    """Handle categorical variable encoding"""

    def __init__(self, log_func=None):
        self.log_func = log_func or self._default_log
        self.encoders = {}

    def _default_log(self, message: str, level: str = "INFO"):
        print(f"[{level}] {message}")

    def label_encode(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Apply label encoding to categorical columns

        Args:
            df: DataFrame
            columns: Columns to encode

        Returns:
            DataFrame with label-encoded columns
        """
        from sklearn.preprocessing import LabelEncoder

        for col in columns:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.encoders[col] = le
                self.log_func(f"Label encoded {col}: {len(le.classes_)} classes")

        return df

    def one_hot_encode(self, df: pd.DataFrame, columns: List[str], drop_first: bool = True) -> pd.DataFrame:
        """
        Apply one-hot encoding

        Args:
            df: DataFrame
            columns: Columns to encode
            drop_first: Drop first category (default True)

        Returns:
            DataFrame with one-hot encoded columns
        """
        df = pd.get_dummies(df, columns=columns, drop_first=drop_first)
        self.log_func(f"One-hot encoded {len(columns)} columns")
        self.log_func(f"New shape: {df.shape}")

        return df


# ============================================================================
# DATA VALIDATION
# ============================================================================

class DataQualityValidator:
    """Validate data quality after cleaning"""

    def __init__(self, log_func=None):
        self.log_func = log_func or self._default_log

    def _default_log(self, message: str, level: str = "INFO"):
        print(f"[{level}] {message}")

    def validate_cleaned_data(self, df: pd.DataFrame) -> Dict:
        """
        Validate cleaned dataset

        Args:
            df: Cleaned DataFrame

        Returns:
            Dictionary with validation results
        """
        results = {
            'shape': df.shape,
            'memory_mb': round(df.memory_usage(deep=True).sum() / (1024**2), 2),
            'missing_pct': round((df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100, 2),
            'duplicate_pct': round((df.duplicated().sum() / len(df)) * 100, 2),
            'duplicates_count': int(df.duplicated().sum()),
            'dtypes': df.dtypes.astype(str).to_dict()
        }

        self.log_func(f"Validation Results:")
        self.log_func(f"  Shape: {results['shape']}")
        self.log_func(f"  Memory: {results['memory_mb']} MB")
        self.log_func(f"  Missing: {results['missing_pct']}%")
        self.log_func(f"  Duplicates: {results['duplicate_pct']}%")

        return results


# ============================================================================
# UTILITIES
# ============================================================================

def generate_cleaning_report(original_df: pd.DataFrame, cleaned_df: pd.DataFrame) -> str:
    """
    Generate data cleaning report

    Args:
        original_df: Original DataFrame before cleaning
        cleaned_df: Cleaned DataFrame

    Returns:
        Formatted report string
    """
    report = "=" * 80 + "\n"
    report += "DATA CLEANING REPORT\n"
    report += "=" * 80 + "\n\n"

    report += "BEFORE CLEANING\n"
    report += f"  Shape: {original_df.shape}\n"
    report += f"  Memory: {original_df.memory_usage(deep=True).sum() / (1024**2):.2f} MB\n"
    report += f"  Missing: {original_df.isnull().sum().sum():,}\n"
    report += f"  Duplicates: {original_df.duplicated().sum()}\n\n"

    report += "AFTER CLEANING\n"
    report += f"  Shape: {cleaned_df.shape}\n"
    report += f"  Memory: {cleaned_df.memory_usage(deep=True).sum() / (1024**2):.2f} MB\n"
    report += f"  Missing: {cleaned_df.isnull().sum().sum():,}\n"
    report += f"  Duplicates: {cleaned_df.duplicated().sum()}\n\n"

    report += "CHANGES\n"
    report += f"  Rows Removed: {original_df.shape[0] - cleaned_df.shape[0]}\n"
    report += f"  Columns Removed: {original_df.shape[1] - cleaned_df.shape[1]}\n"
    report += f"  Memory Reduction: {((original_df.memory_usage(deep=True).sum() - cleaned_df.memory_usage(deep=True).sum()) / original_df.memory_usage(deep=True).sum() * 100):.2f}%\n"

    report += "=" * 80 + "\n"
    return report


if __name__ == "__main__":
    print("Data Cleaning Utility Library - CHUNK_02")
    print("Classes available:")
    print("  - MissingValueHandler")
    print("  - DuplicateHandler")
    print("  - OutlierHandler")
    print("  - DataTypeConverter")
    print("  - CategoricalEncoder")
    print("  - DataQualityValidator")
