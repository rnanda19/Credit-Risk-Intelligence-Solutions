#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
CHUNK_01: DATA INGESTION & PROFILING (INTERACTIVE VERSION)
================================================================================

This version is optimized for Jupyter notebooks and interactive environments.
Can also be run as a regular script.

Usage in Jupyter:
    exec(open('CHUNK_01_INTERACTIVE.py').read())

Usage as script:
    python CHUNK_01_INTERACTIVE.py
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
print("CHUNK_01: DATA INGESTION & PROFILING (INTERACTIVE)")
print("=" * 80 + "\n")

# ============================================================================
# SMART PATH DETECTION
# ============================================================================

def get_chunk01_directory():
    """Intelligently find CHUNK_01_DATA_INGESTION directory"""

    # Try 1: Check if we're in the CHUNK_01 directory
    cwd = os.getcwd()
    if "CHUNK_01_DATA_INGESTION" in cwd:
        return cwd

    # Try 2: Look for CHUNK_01_DATA_INGESTION in current directory
    if os.path.exists("CHUNK_01_DATA_INGESTION"):
        return os.path.abspath("CHUNK_01_DATA_INGESTION")

    # Try 3: Look in parent directory
    if os.path.exists(os.path.join("..", "CHUNK_01_DATA_INGESTION")):
        return os.path.abspath("../CHUNK_01_DATA_INGESTION")

    # Try 4: Windows default path
    windows_path = r"C:\Users\rnand\Documents\home-credit-default-risk\Enterprise_AI_Workflows\PROBLEM_004_Customer_360_Analysis\CHUNK_01_DATA_INGESTION"
    if os.path.exists(windows_path):
        return windows_path

    # Try 5: Use current working directory as fallback
    print(f"[WARNING] Could not find CHUNK_01_DATA_INGESTION. Using: {cwd}")
    return cwd

# Get paths
CHUNK_01_DIR = get_chunk01_directory()
LIB_DIR = os.path.join(CHUNK_01_DIR, "lib")
CONFIG_DIR = os.path.join(CHUNK_01_DIR, "config")
DOCS_DIR = os.path.join(CHUNK_01_DIR, "documentation")
LOGS_DIR = os.path.join(CHUNK_01_DIR, "logs")

# Create directories
for directory in [CONFIG_DIR, DOCS_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

print(f"[OK] CHUNK_01 Directory: {CHUNK_01_DIR}\n")

# ============================================================================
# DATA CONFIGURATION
# ============================================================================

IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    DATA_ROOT = r"C:\Users\rnand\OneDrive\Desktop(1)\home-credit-default-risk\data"
else:
    DATA_ROOT = "/sessions/wonderful-sharp-edison/mnt/data"

print(f"[OK] Data Directory: {DATA_ROOT}\n")

# ============================================================================
# INLINE UTILITY FUNCTIONS (No external imports needed)
# ============================================================================

class DataLoader:
    """Simple data loader for interactive use"""

    def __init__(self, data_root):
        self.data_root = data_root
        self.loaded_data = {}
        self.metadata = {}

    def load_csv(self, filename):
        """Load single CSV file"""
        filepath = os.path.join(self.data_root, filename)

        if not os.path.exists(filepath):
            print(f"[ERROR] File not found: {filename}")
            return None

        try:
            df = pd.read_csv(filepath)
            print(f"[OK] Loaded: {filename} ({len(df):,} rows, {len(df.columns)} cols)")

            self.metadata[filename] = {
                'shape': df.shape,
                'memory_mb': round(df.memory_usage(deep=True).sum() / (1024**2), 2),
                'dtypes': df.dtypes.astype(str).to_dict()
            }

            self.loaded_data[filename] = df
            return df

        except Exception as e:
            print(f"[ERROR] Failed to load {filename}: {str(e)}")
            return None

    def load_all(self, file_list):
        """Load all CSV files"""
        print("=" * 80)
        print("LOADING DATA SOURCES")
        print("=" * 80 + "\n")

        for filename in file_list:
            self.load_csv(filename)

        print(f"\n[OK] Loaded {len(self.loaded_data)}/{len(file_list)} files\n")
        return self.loaded_data


class DataValidator:
    """Simple data validator for interactive use"""

    def validate(self, df, name="Data"):
        """Validate dataset"""
        print(f"Validating: {name}")
        print(f"  Shape: {df.shape}")
        print(f"  Missing: {df.isnull().sum().sum():,} ({(df.isnull().sum().sum()/(df.shape[0]*df.shape[1])*100):.2f}%)")
        print(f"  Duplicates: {df.duplicated().sum():,} ({(df.duplicated().sum()/len(df)*100):.2f}%)")

        return {
            'name': name,
            'shape': df.shape,
            'missing_pct': round((df.isnull().sum().sum()/(df.shape[0]*df.shape[1])*100), 2),
            'duplicate_pct': round((df.duplicated().sum()/len(df)*100), 2)
        }


# ============================================================================
# DATA SOURCES
# ============================================================================

DATA_SOURCES = [
    'application_train.csv',
    'application_test.csv',
    'bureau.csv',
    'bureau_balance.csv',
    'credit_card_balance.csv',
    'installments_payments.csv',
    'POS_CASH_balance.csv',
    'previous_application.csv'
]

# ============================================================================
# EXECUTION
# ============================================================================

def run_chunk01():
    """Execute CHUNK_01"""

    print("=" * 80)
    print("QUALITY GATE 1: DATA INGESTION")
    print("=" * 80 + "\n")

    # Load data
    loader = DataLoader(DATA_ROOT)
    datasets = loader.load_all(DATA_SOURCES)

    if len(datasets) == 0:
        print("[ERROR] No datasets loaded!")
        return None

    print("=" * 80)
    print("QUALITY GATE 2: DATA VALIDATION")
    print("=" * 80 + "\n")

    # Validate data
    validator = DataValidator()
    validation_results = {}

    for filename, df in datasets.items():
        validation_results[filename] = validator.validate(df, filename)

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80 + "\n")

    total_rows = sum(v['shape'][0] for v in validation_results.values())
    total_cols = sum(v['shape'][1] for v in validation_results.values())
    total_memory = sum(loader.metadata[f]['memory_mb'] for f in loader.metadata)

    print(f"Total Rows: {total_rows:,}")
    print(f"Total Columns: {total_cols}")
    print(f"Total Memory: {total_memory:.2f} MB\n")

    # Save metadata
    metadata_path = os.path.join(CONFIG_DIR, 'chunk_01_metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump({
            'datasets': loader.metadata,
            'validation': {k: {'shape': v['shape'], 'missing_pct': v['missing_pct'], 'duplicate_pct': v['duplicate_pct']}
                          for k, v in validation_results.items()},
            'generated_at': datetime.now().isoformat()
        }, f, indent=2, ensure_ascii=False)

    print(f"[OK] Saved metadata: {metadata_path}\n")

    return {
        'datasets': datasets,
        'metadata': loader.metadata,
        'validation': validation_results
    }


# ============================================================================
# RUN IF EXECUTED DIRECTLY
# ============================================================================

if __name__ == "__main__":
    results = run_chunk01()

    print("=" * 80)
    print("CHUNK_01 COMPLETE - READY FOR CHUNK_02")
    print("=" * 80)

# If run in interactive environment, auto-execute
else:
    print("[INFO] Running in interactive environment...\n")
    results = run_chunk01()
