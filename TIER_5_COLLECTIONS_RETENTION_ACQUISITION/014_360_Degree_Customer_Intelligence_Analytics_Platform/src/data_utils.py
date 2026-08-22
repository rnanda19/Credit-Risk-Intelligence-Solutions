#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
CHUNK_01: DATA UTILITY LIBRARY
================================================================================

MODULE: data_utils.py
PURPOSE: Core utility functions for data loading, validation, and profiling
VERSION: 1.0.0
DATE: August 12, 2026

This module provides reusable functions for:
- Data loading from CSV files
- Data validation and quality checks
- Data profiling and exploration
- Data cleaning and transformation
- Memory optimization
- Error handling and logging

================================================================================
"""

import os
import sys
import logging
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import json

# Configure logging
logger = logging.getLogger(__name__)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

class DataLoader:
    """Handles loading and validation of CSV data sources"""

    def __init__(self, data_root: str, log_func=None):
        """
        Initialize DataLoader

        Args:
            data_root: Root directory containing CSV files
            log_func: Optional logging function
        """
        self.data_root = data_root
        self.log_func = log_func or self._default_log
        self.loaded_data = {}
        self.load_metadata = {}

    def _default_log(self, message: str, level: str = "INFO"):
        """Default logging function"""
        print(f"[{level}] {message}")

    def load_csv(self, filename: str, sample: bool = False,
                 sample_size: int = 10000) -> Optional[pd.DataFrame]:
        """
        Load CSV file with error handling

        Args:
            filename: Name of CSV file
            sample: Whether to load sample instead of full data
            sample_size: Number of rows to sample

        Returns:
            Loaded DataFrame or None if error
        """
        filepath = os.path.join(self.data_root, filename)

        if not os.path.exists(filepath):
            self.log_func(f"[ERROR] File not found: {filename}", "ERROR")
            return None

        try:
            if sample:
                df = pd.read_csv(filepath, nrows=sample_size)
                self.log_func(f"[OK] Loaded sample: {filename} ({len(df)} rows)")
            else:
                df = pd.read_csv(filepath)
                self.log_func(f"[OK] Loaded: {filename} ({len(df)} rows)")

            # Store metadata
            self.load_metadata[filename] = {
                'shape': df.shape,
                'memory_mb': df.memory_usage(deep=True).sum() / (1024**2),
                'columns': list(df.columns),
                'dtypes': df.dtypes.astype(str).to_dict(),
                'load_time': datetime.now().isoformat(),
                'sample': sample
            }

            self.loaded_data[filename] = df
            return df

        except Exception as e:
            self.log_func(f"[ERROR] Failed to load {filename}: {str(e)}", "ERROR")
            return None

    def load_all_datasets(self, file_list: List[str]) -> Dict[str, pd.DataFrame]:
        """
        Load multiple CSV files

        Args:
            file_list: List of CSV filenames

        Returns:
            Dictionary of loaded DataFrames
        """
        self.log_func("\n" + "=" * 80)
        self.log_func("LOADING DATA SOURCES")
        self.log_func("=" * 80)

        for filename in file_list:
            self.load_csv(filename)

        self.log_func(f"\n[OK] Loaded {len(self.loaded_data)}/{len(file_list)} files\n")
        return self.loaded_data

    def get_dataframe(self, filename: str) -> Optional[pd.DataFrame]:
        """Retrieve loaded DataFrame"""
        return self.loaded_data.get(filename)


# ============================================================================
# DATA VALIDATION FUNCTIONS
# ============================================================================

class DataValidator:
    """Validates data quality and integrity"""

    def __init__(self, log_func=None):
        """
        Initialize DataValidator

        Args:
            log_func: Optional logging function
        """
        self.log_func = log_func or self._default_log
        self.validation_results = {}

    def _default_log(self, message: str, level: str = "INFO"):
        """Default logging function"""
        print(f"[{level}] {message}")

    def check_missing_values(self, df: pd.DataFrame, name: str = "Data") -> Dict:
        """
        Check for missing values

        Args:
            df: DataFrame to check
            name: Name for reporting

        Returns:
            Dictionary with missing value statistics
        """
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        missing_pct = (missing_cells / total_cells) * 100

        missing_by_col = df.isnull().sum()
        missing_by_col_pct = (missing_by_col / len(df)) * 100

        result = {
            'total_missing': int(missing_cells),
            'missing_pct': round(missing_pct, 2),
            'by_column': missing_by_col.to_dict(),
            'by_column_pct': missing_by_col_pct.to_dict()
        }

        self.log_func(f"  Missing values: {missing_cells} ({missing_pct:.2f}%)")
        return result

    def check_duplicates(self, df: pd.DataFrame, name: str = "Data") -> Dict:
        """
        Check for duplicate rows

        Args:
            df: DataFrame to check
            name: Name for reporting

        Returns:
            Dictionary with duplicate statistics
        """
        total_dupes = df.duplicated().sum()
        complete_dupes = df.duplicated(keep=False).sum()
        dupe_pct = (total_dupes / len(df)) * 100

        result = {
            'total_duplicates': int(total_dupes),
            'complete_duplicates': int(complete_dupes),
            'duplicate_pct': round(dupe_pct, 2)
        }

        self.log_func(f"  Duplicates: {total_dupes} ({dupe_pct:.2f}%)")
        return result

    def check_data_types(self, df: pd.DataFrame) -> Dict:
        """
        Analyze data types

        Args:
            df: DataFrame to analyze

        Returns:
            Dictionary with data type information
        """
        dtype_counts = df.dtypes.value_counts().to_dict()
        dtype_names = {str(k): v for k, v in dtype_counts.items()}

        result = {
            'total_columns': len(df.columns),
            'dtype_distribution': dtype_names,
            'column_dtypes': df.dtypes.astype(str).to_dict()
        }

        self.log_func(f"  Data types: {dtype_names}")
        return result

    def validate_dataset(self, df: pd.DataFrame, name: str = "Data") -> Dict:
        """
        Run comprehensive validation

        Args:
            df: DataFrame to validate
            name: Name for reporting

        Returns:
            Complete validation results
        """
        self.log_func(f"\nValidating: {name}")
        self.log_func(f"  Shape: {df.shape[0]} rows, {df.shape[1]} columns")

        results = {
            'name': name,
            'shape': df.shape,
            'memory_mb': round(df.memory_usage(deep=True).sum() / (1024**2), 2),
            'missing_values': self.check_missing_values(df, name),
            'duplicates': self.check_duplicates(df, name),
            'data_types': self.check_data_types(df)
        }

        return results


# ============================================================================
# DATA PROFILING FUNCTIONS
# ============================================================================

class DataProfiler:
    """Generates detailed data profiles"""

    def __init__(self, log_func=None):
        """
        Initialize DataProfiler

        Args:
            log_func: Optional logging function
        """
        self.log_func = log_func or self._default_log
        self.profiles = {}

    def _default_log(self, message: str, level: str = "INFO"):
        """Default logging function"""
        print(f"[{level}] {message}")

    def profile_numeric_column(self, series: pd.Series) -> Dict:
        """
        Profile numeric column

        Args:
            series: Numeric Series to profile

        Returns:
            Dictionary with numeric statistics
        """
        return {
            'dtype': str(series.dtype),
            'non_null': int(series.notna().sum()),
            'null': int(series.isnull().sum()),
            'null_pct': round((series.isnull().sum() / len(series)) * 100, 2),
            'unique': int(series.nunique()),
            'min': float(series.min()) if len(series) > 0 else None,
            'max': float(series.max()) if len(series) > 0 else None,
            'mean': float(series.mean()) if len(series) > 0 else None,
            'median': float(series.median()) if len(series) > 0 else None,
            'std': float(series.std()) if len(series) > 0 else None,
            'skewness': float(series.skew()) if len(series) > 0 else None
        }

    def profile_categorical_column(self, series: pd.Series, top_n: int = 10) -> Dict:
        """
        Profile categorical column

        Args:
            series: Categorical Series to profile
            top_n: Number of top categories to show

        Returns:
            Dictionary with categorical statistics
        """
        value_counts = series.value_counts().head(top_n)

        return {
            'dtype': str(series.dtype),
            'non_null': int(series.notna().sum()),
            'null': int(series.isnull().sum()),
            'null_pct': round((series.isnull().sum() / len(series)) * 100, 2),
            'unique': int(series.nunique()),
            'top_values': value_counts.to_dict()
        }

    def profile_dataframe(self, df: pd.DataFrame, name: str = "Data") -> Dict:
        """
        Profile entire DataFrame

        Args:
            df: DataFrame to profile
            name: Name for reporting

        Returns:
            Dictionary with complete profile
        """
        self.log_func(f"\nProfiling: {name}")

        profile = {
            'name': name,
            'shape': df.shape,
            'columns': {}
        }

        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                profile['columns'][col] = self.profile_numeric_column(df[col])
            else:
                profile['columns'][col] = self.profile_categorical_column(df[col])

        self.profiles[name] = profile
        self.log_func(f"[OK] Profiled {len(df.columns)} columns")

        return profile


# ============================================================================
# DATA QUALITY REPORT FUNCTIONS
# ============================================================================

class DataQualityReporter:
    """Generates data quality reports"""

    def __init__(self, log_func=None):
        """Initialize DataQualityReporter"""
        self.log_func = log_func or self._default_log

    def _default_log(self, message: str, level: str = "INFO"):
        """Default logging function"""
        print(f"[{level}] {message}")

    def generate_summary_report(self, datasets_info: Dict) -> str:
        """
        Generate summary report for all datasets

        Args:
            datasets_info: Dictionary with dataset information

        Returns:
            Formatted report string
        """
        report = "=" * 80 + "\n"
        report += "DATA INGESTION & PROFILING SUMMARY\n"
        report += "=" * 80 + "\n\n"

        report += "DATASETS LOADED\n"
        report += "-" * 80 + "\n"

        total_rows = 0
        total_cols = 0
        total_memory = 0

        for filename, info in datasets_info.items():
            rows, cols = info['shape']
            memory = info.get('memory_mb', 0)

            report += f"\n{filename}\n"
            report += f"  Rows: {rows:,}\n"
            report += f"  Columns: {cols}\n"
            report += f"  Memory: {memory:.2f} MB\n"

            total_rows += rows
            total_cols += cols
            total_memory += memory

        report += "\n" + "-" * 80 + "\n"
        report += f"TOTAL ROWS: {total_rows:,}\n"
        report += f"TOTAL COLUMNS: {total_cols}\n"
        report += f"TOTAL MEMORY: {total_memory:.2f} MB\n"
        report += "=" * 80 + "\n"

        return report

    def generate_quality_report(self, validation_results: Dict) -> str:
        """
        Generate quality report

        Args:
            validation_results: Dictionary with validation results

        Returns:
            Formatted quality report
        """
        report = "=" * 80 + "\n"
        report += "DATA QUALITY REPORT\n"
        report += "=" * 80 + "\n"

        for dataset_name, results in validation_results.items():
            report += f"\n{dataset_name}\n"
            report += "-" * 80 + "\n"

            # Missing values
            missing = results.get('missing_values', {})
            report += f"Missing Values: {missing.get('missing_pct', 0)}%\n"

            # Duplicates
            dupes = results.get('duplicates', {})
            report += f"Duplicates: {dupes.get('duplicate_pct', 0)}%\n"

            # Data types
            dtypes = results.get('data_types', {})
            report += f"Data Types: {dtypes.get('dtype_distribution', {})}\n"

            report += "\n"

        report += "=" * 80 + "\n"
        return report


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimize DataFrame memory usage by converting dtypes

    Args:
        df: DataFrame to optimize

    Returns:
        DataFrame with optimized dtypes
    """
    original_memory = df.memory_usage(deep=True).sum() / (1024**2)

    for col in df.columns:
        col_type = df[col].dtype

        if col_type == 'object':
            continue

        elif col_type == 'int64':
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

    print(f"[OK] Memory optimization: {original_memory:.2f}MB -> {optimized_memory:.2f}MB ({reduction:.1f}% reduction)")

    return df


def save_to_parquet(df: pd.DataFrame, filepath: str) -> bool:
    """
    Save DataFrame to Parquet format

    Args:
        df: DataFrame to save
        filepath: Path to save file

    Returns:
        True if successful
    """
    try:
        df.to_parquet(filepath, index=False, compression='snappy')
        print(f"[OK] Saved: {filepath}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save: {str(e)}")
        return False


def load_from_parquet(filepath: str) -> Optional[pd.DataFrame]:
    """
    Load DataFrame from Parquet

    Args:
        filepath: Path to Parquet file

    Returns:
        Loaded DataFrame or None
    """
    try:
        df = pd.read_parquet(filepath)
        print(f"[OK] Loaded: {filepath}")
        return df
    except Exception as e:
        print(f"[ERROR] Failed to load: {str(e)}")
        return None


# ============================================================================
# MODULE INITIALIZATION
# ============================================================================

if __name__ == "__main__":
    print("Data Utils Library - CHUNK_01")
    print("This module provides utility functions for data operations")
    print("\nAvailable classes:")
    print("  - DataLoader: Load CSV files")
    print("  - DataValidator: Validate data quality")
    print("  - DataProfiler: Profile data characteristics")
    print("  - DataQualityReporter: Generate quality reports")
