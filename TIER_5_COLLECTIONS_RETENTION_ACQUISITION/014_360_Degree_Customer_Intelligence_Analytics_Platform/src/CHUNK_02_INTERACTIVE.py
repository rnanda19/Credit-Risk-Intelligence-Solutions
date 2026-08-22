#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
CHUNK_02: DATA CLEANING & PREPROCESSING (INTERACTIVE VERSION)
================================================================================

This version is optimized for Jupyter notebooks and interactive environments.

Usage in Jupyter:
    # Load data from CHUNK_01 first
    datasets = results['datasets']  # From CHUNK_01

    # Then run:
    exec(open('CHUNK_02_INTERACTIVE.py').read())
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

print("\n" + "=" * 80)
print("CHUNK_02: DATA CLEANING & PREPROCESSING (INTERACTIVE)")
print("=" * 80 + "\n")

# ============================================================================
# PATH SETUP
# ============================================================================

def get_chunk02_directory():
    """Find CHUNK_02_DATA_CLEANING directory"""
    cwd = os.getcwd()

    if "CHUNK_02_DATA_CLEANING" in cwd:
        return cwd
    if os.path.exists("CHUNK_02_DATA_CLEANING"):
        return os.path.abspath("CHUNK_02_DATA_CLEANING")
    if os.path.exists(os.path.join("..", "CHUNK_02_DATA_CLEANING")):
        return os.path.abspath("../CHUNK_02_DATA_CLEANING")

    windows_path = r"C:\Users\rnand\Documents\home-credit-default-risk\Enterprise_AI_Workflows\PROBLEM_004_Customer_360_Analysis\CHUNK_02_DATA_CLEANING"
    if os.path.exists(windows_path):
        return windows_path

    return cwd

CHUNK_02_DIR = get_chunk02_directory()
LIB_DIR = os.path.join(CHUNK_02_DIR, "lib")
CONFIG_DIR = os.path.join(CHUNK_02_DIR, "config")
DOCS_DIR = os.path.join(CHUNK_02_DIR, "documentation")
LOGS_DIR = os.path.join(CHUNK_02_DIR, "logs")

for directory in [CONFIG_DIR, DOCS_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

print(f"[OK] CHUNK_02 Directory: {CHUNK_02_DIR}\n")

# ============================================================================
# IMPORT CLEANING LIBRARY
# ============================================================================

sys.path.insert(0, LIB_DIR)

try:
    from data_cleaning import (
        MissingValueHandler, DuplicateHandler, OutlierHandler,
        DataTypeConverter, CategoricalEncoder, DataQualityValidator,
        generate_cleaning_report
    )
    print("[OK] Imported data_cleaning library\n")
except ImportError as e:
    print(f"[WARNING] Could not import data_cleaning: {e}")
    print("[INFO] Creating inline versions...\n")

    # Fallback: Simple inline versions
    class MissingValueHandler:
        def __init__(self, log_func=None):
            self.log_func = log_func or print

        def analyze_missing(self, df):
            missing_counts = df.isnull().sum()
            return {
                'total_missing': int(missing_counts.sum()),
                'by_column': missing_counts[missing_counts > 0].to_dict()
            }

        def drop_high_missing_columns(self, df, threshold=50.0):
            missing_pct = (df.isnull().sum() / len(df)) * 100
            cols_to_drop = missing_pct[missing_pct > threshold].index.tolist()
            if cols_to_drop:
                df = df.drop(columns=cols_to_drop)
                self.log_func(f"[OK] Dropped {len(cols_to_drop)} high-missing columns")
            return df

        def fill_missing_numeric(self, df, method='median'):
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if df[col].isnull().sum() > 0:
                    df[col].fillna(df[col].median(), inplace=True)
            self.log_func(f"[OK] Filled numeric missing values using {method}")
            return df

        def fill_missing_categorical(self, df, method='mode'):
            cat_cols = df.select_dtypes(include=['object']).columns
            for col in cat_cols:
                if df[col].isnull().sum() > 0:
                    df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 'MISSING', inplace=True)
            self.log_func(f"[OK] Filled categorical missing values using {method}")
            return df

    class DuplicateHandler:
        def __init__(self, log_func=None):
            self.log_func = log_func or print

        def remove_duplicates(self, df, subset=None, keep='first'):
            initial_rows = len(df)
            df = df.drop_duplicates(subset=subset, keep=keep)
            removed = initial_rows - len(df)
            if removed > 0:
                self.log_func(f"[OK] Removed {removed} duplicate rows")
            return df

    class DataQualityValidator:
        def __init__(self, log_func=None):
            self.log_func = log_func or print

        def validate_cleaned_data(self, df):
            results = {
                'shape': df.shape,
                'memory_mb': round(df.memory_usage(deep=True).sum() / (1024**2), 2),
                'missing_pct': round((df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100, 2),
                'duplicate_pct': round((df.duplicated().sum() / len(df)) * 100, 2)
            }
            return results

# ============================================================================
# DATA CLEANING EXECUTION
# ============================================================================

def clean_datasets(datasets):
    """
    Clean all datasets from CHUNK_01

    Args:
        datasets: Dictionary of DataFrames from CHUNK_01

    Returns:
        Dictionary of cleaned DataFrames
    """
    print("=" * 80)
    print("QUALITY GATE 1: HANDLE MISSING VALUES")
    print("=" * 80 + "\n")

    missing_handler = MissingValueHandler()
    cleaned_datasets = {}

    for filename, df in datasets.items():
        print(f"\nCleaning: {filename}")

        # Analyze missing
        missing_analysis = missing_handler.analyze_missing(df)
        print(f"  Total missing: {missing_analysis['total_missing']:,} ({missing_analysis['total_missing_pct']:.2f}%)")

        # Drop high-missing columns
        df = missing_handler.drop_high_missing_columns(df, threshold=50.0)

        # Fill remaining missing values
        df = missing_handler.fill_missing_numeric(df, method='median')
        df = missing_handler.fill_missing_categorical(df, method='mode')

        cleaned_datasets[filename] = df

    print("\n" + "=" * 80)
    print("QUALITY GATE 2: HANDLE DUPLICATES")
    print("=" * 80 + "\n")

    dup_handler = DuplicateHandler()

    for filename, df in cleaned_datasets.items():
        initial_rows = len(df)
        df = dup_handler.remove_duplicates(df)
        cleaned_datasets[filename] = df

    print("\n" + "=" * 80)
    print("QUALITY GATE 3: VALIDATE CLEANED DATA")
    print("=" * 80 + "\n")

    validator = DataQualityValidator()
    validation_results = {}

    for filename, df in cleaned_datasets.items():
        validation = validator.validate_cleaned_data(df)
        validation_results[filename] = validation

        print(f"\n{filename}")
        print(f"  Shape: {validation['shape']}")
        print(f"  Memory: {validation['memory_mb']:.2f} MB")
        print(f"  Missing: {validation['missing_pct']:.2f}%")
        print(f"  Duplicates: {validation['duplicate_pct']:.2f}%")

    return cleaned_datasets, validation_results


def generate_cleaning_summary(datasets, cleaned_datasets, validation_results):
    """Generate cleaning summary report"""

    print("\n" + "=" * 80)
    print("GENERATING REPORTS")
    print("=" * 80 + "\n")

    summary = "=" * 80 + "\n"
    summary += "DATA CLEANING SUMMARY\n"
    summary += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    summary += "=" * 80 + "\n\n"

    for filename in datasets.keys():
        original = datasets[filename]
        cleaned = cleaned_datasets[filename]
        validation = validation_results[filename]

        summary += f"\n{filename}\n"
        summary += "-" * 80 + "\n"
        summary += f"Before: {original.shape[0]:,} rows, {original.shape[1]} cols\n"
        summary += f"After:  {cleaned.shape[0]:,} rows, {cleaned.shape[1]} cols\n"
        summary += f"Removed: {original.shape[0] - cleaned.shape[0]:,} rows, {original.shape[1] - cleaned.shape[1]} cols\n"
        summary += f"Quality: {validation['missing_pct']:.2f}% missing, {validation['duplicate_pct']:.2f}% duplicates\n"

    summary += "\n" + "=" * 80 + "\n"
    return summary


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_chunk02(datasets=None):
    """
    Execute CHUNK_02

    Args:
        datasets: Dictionary of DataFrames from CHUNK_01
                 If None, tries to load from CHUNK_01 results
    """

    # Try to get datasets from CHUNK_01 results
    if datasets is None:
        try:
            if 'results' in globals():
                datasets = results['datasets']
                print("[OK] Using datasets from CHUNK_01 results\n")
            else:
                print("[ERROR] No datasets provided. Run CHUNK_01 first.")
                return None
        except:
            print("[ERROR] Could not access CHUNK_01 results")
            return None

    # Run cleaning pipeline
    cleaned_datasets, validation_results = clean_datasets(datasets)

    # Generate reports
    summary = generate_cleaning_summary(datasets, cleaned_datasets, validation_results)

    # Save results
    summary_path = os.path.join(DOCS_DIR, 'CHUNK_02_CLEANING_SUMMARY.txt')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f"\n[OK] Saved summary: {summary_path}")

    # Save metadata
    metadata = {
        'generated_at': datetime.now().isoformat(),
        'datasets': {},
        'validation': validation_results
    }

    for filename, df in cleaned_datasets.items():
        metadata['datasets'][filename] = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.astype(str).to_dict()
        }

    metadata_path = os.path.join(CONFIG_DIR, 'chunk_02_metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"[OK] Saved metadata: {metadata_path}\n")

    print("=" * 80)
    print("CHUNK_02: DATA CLEANING COMPLETE")
    print("=" * 80 + "\n")

    print("Ready for CHUNK_03 - Feature Validation\n")

    return {
        'cleaned_datasets': cleaned_datasets,
        'validation_results': validation_results,
        'summary': summary
    }


# ============================================================================
# AUTO-RUN IN INTERACTIVE MODE
# ============================================================================

if __name__ == "__main__":
    # Try to access results from CHUNK_01
    try:
        if 'results' in globals():
            chunk02_results = run_chunk02(datasets=results['datasets'])
        else:
            print("[INFO] No datasets available. Please run CHUNK_01 first.")
    except NameError:
        print("[INFO] Running in script mode. Please provide datasets.")
else:
    # Interactive mode
    try:
        chunk02_results = run_chunk02()
    except:
        print("[INFO] Run with datasets from CHUNK_01:\n")
        print("    chunk02_results = run_chunk02(datasets=results['datasets'])\n")
