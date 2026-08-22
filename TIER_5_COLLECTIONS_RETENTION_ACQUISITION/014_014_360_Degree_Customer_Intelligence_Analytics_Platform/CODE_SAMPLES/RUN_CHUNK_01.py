#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CHUNK_01: DATA INGESTION & PROFILING - CROSS-PLATFORM RUNNER
================================================================================

Works on Windows, Linux, and macOS

Usage:
    python RUN_CHUNK_01.py
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("\n" + "=" * 80)
    print(" PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS")
    print(" CHUNK_01: DATA INGESTION AND PROFILING")
    print("=" * 80 + "\n")

    current_dir = Path(__file__).parent
    script_path = current_dir / "scripts" / "CHUNK_01_DATA_INGESTION.py"

    if not script_path.exists():
        print(f"ERROR: Script not found at {script_path}")
        return 1

    print(f"Project Root: {current_dir.parent}")
    print(f"Running: {script_path}\n")
    print("This will:")
    print("  1. Load all 8 CSV datasets (1.4 GB)")
    print("  2. Validate data quality")
    print("  3. Profile data characteristics")
    print("  4. Generate data dictionary")
    print("  5. Create quality reports\n")

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(current_dir),
            check=False
        )

        if result.returncode == 0:
            print("\n" + "=" * 80)
            print(" CHUNK_01 EXECUTION COMPLETE")
            print("=" * 80 + "\n")
            print("Generated outputs:")
            print("  - documentation/INGESTION_SUMMARY.txt")
            print("  - documentation/DATA_QUALITY_REPORT.txt")
            print("  - documentation/CHUNK_01_DETAILED_REPORT.md")
            print("  - config/data_dictionary.json")
            print("  - logs/chunk_01_execution.log\n")
            print("Available Library Functions:")
            print("  - DataLoader: Load CSV files")
            print("  - DataValidator: Check data quality")
            print("  - DataProfiler: Profile data characteristics")
            print("  - DataQualityReporter: Generate reports\n")
            print("Ready to proceed to CHUNK_02 - Data Cleaning\n")
            return 0
        else:
            print("\n" + "=" * 80)
            print(" ERROR: Script execution failed!")
            print("=" * 80 + "\n")
            return 1

    except Exception as e:
        print(f"\nERROR: Failed to run script: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
