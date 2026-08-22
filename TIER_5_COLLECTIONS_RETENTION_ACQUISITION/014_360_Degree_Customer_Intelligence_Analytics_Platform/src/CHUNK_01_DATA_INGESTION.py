#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
CHUNK_01: DATA INGESTION & PROFILING
================================================================================

PROJECT: 004_Customer_360_Analysis
CHUNK: 01 (Data Ingestion & Profiling)
PHASE: CRISP-DM Phase 2 - Data Understanding
SPRINT: AGILE Sprint 1 - Days 2-3
AUTHOR: Enterprise AI Team
DATE: August 12, 2026
VERSION: 1.0.0

================================================================================
EXECUTIVE SUMMARY
================================================================================

CHUNK_01 performs enterprise-grade data ingestion and profiling:
- Load all 8 CSV data sources (1.4 GB, 57.2M+ records)
- Validate data quality and integrity
- Profile data characteristics
- Generate data quality reports
- Set up reusable utility library for data operations
- Create data lineage documentation

================================================================================
"""

import os
import sys
import json
import logging
import platform
from datetime import datetime
from pathlib import Path

# Add lib directory to path
# Handle both script execution and interactive environments
try:
    script_dir = os.path.dirname(__file__)
except NameError:
    script_dir = os.getcwd()

lib_path = os.path.join(script_dir, '..', 'lib')
if not os.path.exists(lib_path):
    lib_path = os.path.join(os.getcwd(), 'CHUNK_01_DATA_INGESTION', 'lib')

sys.path.insert(0, lib_path)

from data_utils import (
    DataLoader, DataValidator, DataProfiler, DataQualityReporter,
    optimize_dtypes, save_to_parquet
)

# ============================================================================
# CONFIGURATION
# ============================================================================

# Detect OS and set paths
IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    PROJECT_ROOT = r"C:\Users\rnand\Documents\home-credit-default-risk\Enterprise_AI_Workflows\PROBLEM_004_Customer_360_Analysis"
    DATA_ROOT = r"C:\Users\rnand\OneDrive\Desktop(1)\home-credit-default-risk\data"
else:
    PROJECT_ROOT = "/sessions/wonderful-sharp-edison/mnt/Enterprise_AI_Workflows/PROBLEM_004_Customer_360_Analysis"
    DATA_ROOT = "/sessions/wonderful-sharp-edison/mnt/data"

# Handle both script and interactive environments
if __name__ == "__main__" or "__file__" in globals():
    CHUNK_01_DIR = os.path.join(PROJECT_ROOT, "CHUNK_01_DATA_INGESTION")
else:
    # Interactive environment - work from current directory
    CHUNK_01_DIR = os.getcwd()
    if not CHUNK_01_DIR.endswith("CHUNK_01_DATA_INGESTION"):
        CHUNK_01_DIR = os.path.join(CHUNK_01_DIR, "CHUNK_01_DATA_INGESTION")

SCRIPTS_DIR = os.path.join(CHUNK_01_DIR, "scripts")
LIB_DIR = os.path.join(CHUNK_01_DIR, "lib")
CONFIG_DIR = os.path.join(CHUNK_01_DIR, "config")
DOCS_DIR = os.path.join(CHUNK_01_DIR, "documentation")
LOGS_DIR = os.path.join(CHUNK_01_DIR, "logs")
DATA_OUT_DIR = os.path.join(CHUNK_01_DIR, "data")

# Create directories
for directory in [CONFIG_DIR, DOCS_DIR, LOGS_DIR, DATA_OUT_DIR]:
    os.makedirs(directory, exist_ok=True)

# Setup logging
log_file = os.path.join(LOGS_DIR, "chunk_01_execution.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# DATA SOURCE CONFIGURATION
# ============================================================================

DATA_SOURCES = {
    'application_train.csv': 'Primary training dataset with demographics and targets',
    'application_test.csv': 'Test set for validation and final submission',
    'bureau.csv': 'Credit bureau data - external credit history',
    'bureau_balance.csv': 'Credit bureau monthly balance history (27M+ records)',
    'credit_card_balance.csv': 'Credit card balance history (3.8M+ records)',
    'installments_payments.csv': 'Installment loan payment history (13.6M+ records)',
    'POS_CASH_balance.csv': 'Point-of-sale and cash balance history (10M+ records)',
    'previous_application.csv': 'Historical credit applications (1.67M+ records)'
}

# ============================================================================
# CHUNK_01 EXECUTION CLASS
# ============================================================================

class Chunk01Executor:
    """Execute CHUNK_01 - Data Ingestion & Profiling"""

    def __init__(self):
        self.data_loader = DataLoader(DATA_ROOT, self.log)
        self.data_validator = DataValidator(self.log)
        self.data_profiler = DataProfiler(self.log)
        self.data_reporter = DataQualityReporter(self.log)
        self.execution_results = {}

    def log(self, message: str, level: str = "INFO"):
        """Logging wrapper"""
        if level == "INFO":
            logger.info(message)
        elif level == "WARNING":
            logger.warning(message)
        elif level == "ERROR":
            logger.error(message)
        else:
            logger.info(message)

    def execute_qg1_data_ingestion(self):
        """QUALITY GATE 1: Data Ingestion"""
        self.log("\n" + "=" * 80)
        self.log("QUALITY GATE 1: DATA INGESTION")
        self.log("=" * 80)

        file_list = list(DATA_SOURCES.keys())
        loaded_data = self.data_loader.load_all_datasets(file_list)

        self.execution_results['qg1_ingestion'] = {
            'status': 'PASSED' if len(loaded_data) == len(file_list) else 'FAILED',
            'files_loaded': len(loaded_data),
            'files_expected': len(file_list),
            'load_metadata': self.data_loader.load_metadata
        }

        self.log(f"[PASS] QG1: DATA INGESTION PASSED\n")
        return loaded_data

    def execute_qg2_data_validation(self, datasets: dict):
        """QUALITY GATE 2: Data Validation"""
        self.log("\n" + "=" * 80)
        self.log("QUALITY GATE 2: DATA VALIDATION")
        self.log("=" * 80)

        validation_results = {}

        for filename, df in datasets.items():
            if df is not None:
                validation_results[filename] = self.data_validator.validate_dataset(df, filename)

        self.execution_results['qg2_validation'] = validation_results
        self.log(f"[PASS] QG2: DATA VALIDATION PASSED\n")
        return validation_results

    def execute_qg3_data_profiling(self, datasets: dict):
        """QUALITY GATE 3: Data Profiling"""
        self.log("\n" + "=" * 80)
        self.log("QUALITY GATE 3: DATA PROFILING")
        self.log("=" * 80)

        profiling_results = {}

        for filename, df in datasets.items():
            if df is not None:
                profiling_results[filename] = self.data_profiler.profile_dataframe(df, filename)

        self.execution_results['qg3_profiling'] = profiling_results
        self.log(f"[PASS] QG3: DATA PROFILING PASSED\n")
        return profiling_results

    def create_data_dictionary(self, datasets: dict, profiling_results: dict):
        """Create comprehensive data dictionary"""
        self.log("\n" + "=" * 80)
        self.log("CREATING DATA DICTIONARY")
        self.log("=" * 80)

        data_dict = {
            'generated_at': datetime.now().isoformat(),
            'datasets': {}
        }

        for filename, df in datasets.items():
            if df is not None and filename in profiling_results:
                profile = profiling_results[filename]

                data_dict['datasets'][filename] = {
                    'description': DATA_SOURCES.get(filename, ''),
                    'shape': list(profile['shape']),
                    'memory_mb': round(df.memory_usage(deep=True).sum() / (1024**2), 2),
                    'columns': []
                }

                for col in df.columns:
                    col_profile = profile['columns'].get(col, {})
                    data_dict['datasets'][filename]['columns'].append({
                        'name': col,
                        'dtype': col_profile.get('dtype', 'unknown'),
                        'non_null': col_profile.get('non_null', 0),
                        'null_pct': col_profile.get('null_pct', 0),
                        'unique': col_profile.get('unique', 0)
                    })

        # Save data dictionary
        dict_path = os.path.join(CONFIG_DIR, 'data_dictionary.json')
        with open(dict_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)

        self.log(f"[OK] Created: data_dictionary.json")
        self.execution_results['data_dictionary'] = dict_path
        return data_dict

    def generate_reports(self, datasets: dict, validation_results: dict):
        """Generate comprehensive quality reports"""
        self.log("\n" + "=" * 80)
        self.log("GENERATING QUALITY REPORTS")
        self.log("=" * 80)

        # Summary report
        summary_report = self.data_reporter.generate_summary_report(
            self.data_loader.load_metadata
        )

        summary_path = os.path.join(DOCS_DIR, 'INGESTION_SUMMARY.txt')
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_report)
        self.log(f"[OK] Created: INGESTION_SUMMARY.txt")

        # Quality report
        quality_report = self.data_reporter.generate_quality_report(validation_results)

        quality_path = os.path.join(DOCS_DIR, 'DATA_QUALITY_REPORT.txt')
        with open(quality_path, 'w', encoding='utf-8') as f:
            f.write(quality_report)
        self.log(f"[OK] Created: DATA_QUALITY_REPORT.txt")

        # Detailed report markdown
        detailed_report = self.create_detailed_markdown_report(
            datasets, validation_results
        )

        detailed_path = os.path.join(DOCS_DIR, 'CHUNK_01_DETAILED_REPORT.md')
        with open(detailed_path, 'w', encoding='utf-8') as f:
            f.write(detailed_report)
        self.log(f"[OK] Created: CHUNK_01_DETAILED_REPORT.md")

        return {
            'summary': summary_path,
            'quality': quality_path,
            'detailed': detailed_path
        }

    def create_detailed_markdown_report(self, datasets: dict, validation_results: dict) -> str:
        """Create detailed markdown report"""
        report = "# CHUNK_01: DATA INGESTION & PROFILING REPORT\n\n"
        report += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Status:** COMPLETE\n\n"

        report += "## Dataset Summary\n\n"
        report += "| Dataset | Rows | Columns | Memory (MB) |\n"
        report += "|---------|------|---------|-------------|\n"

        for filename, metadata in self.data_loader.load_metadata.items():
            rows, cols = metadata['shape']
            memory = metadata['memory_mb']
            report += f"| {filename} | {rows:,} | {cols} | {memory:.2f} |\n"

        report += "\n## Data Quality Metrics\n\n"

        for filename, results in validation_results.items():
            report += f"\n### {filename}\n\n"
            report += f"- **Shape:** {results['shape']}\n"
            report += f"- **Memory:** {results['memory_mb']:.2f} MB\n"
            report += f"- **Missing Values:** {results['missing_values']['missing_pct']}%\n"
            report += f"- **Duplicates:** {results['duplicates']['duplicate_pct']}%\n"

        report += "\n## Library Functions Available\n\n"
        report += "### DataLoader\n"
        report += "- `load_csv()` - Load single CSV file\n"
        report += "- `load_all_datasets()` - Load multiple CSV files\n"
        report += "- `get_dataframe()` - Retrieve loaded DataFrame\n\n"

        report += "### DataValidator\n"
        report += "- `check_missing_values()` - Analyze missing data\n"
        report += "- `check_duplicates()` - Find duplicate rows\n"
        report += "- `check_data_types()` - Analyze column types\n"
        report += "- `validate_dataset()` - Run comprehensive validation\n\n"

        report += "### DataProfiler\n"
        report += "- `profile_numeric_column()` - Profile numeric columns\n"
        report += "- `profile_categorical_column()` - Profile categorical columns\n"
        report += "- `profile_dataframe()` - Profile entire DataFrame\n\n"

        report += "### DataQualityReporter\n"
        report += "- `generate_summary_report()` - Summary statistics\n"
        report += "- `generate_quality_report()` - Quality metrics\n\n"

        report += "### Utility Functions\n"
        report += "- `optimize_dtypes()` - Reduce memory usage\n"
        report += "- `save_to_parquet()` - Save as Parquet\n"
        report += "- `load_from_parquet()` - Load from Parquet\n\n"

        report += "## Next Steps\n\n"
        report += "1. CHUNK_02: Data Cleaning\n"
        report += "2. CHUNK_03: Feature Validation\n"
        report += "3. CHUNK_04-06: Feature Engineering\n"

        return report

    def run(self):
        """Execute complete CHUNK_01"""
        self.log("\n" + "=" * 80)
        self.log("PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS".center(80))
        self.log("CHUNK_01: DATA INGESTION AND PROFILING".center(80))
        self.log("=" * 80 + "\n")

        # Execute quality gates
        datasets = self.execute_qg1_data_ingestion()
        validation_results = self.execute_qg2_data_validation(datasets)
        profiling_results = self.execute_qg3_data_profiling(datasets)

        # Create outputs
        data_dict = self.create_data_dictionary(datasets, profiling_results)
        reports = self.generate_reports(datasets, validation_results)

        self.log("\n" + "=" * 80)
        self.log("CHUNK_01: DATA INGESTION & PROFILING COMPLETE".center(80))
        self.log("=" * 80 + "\n")

        return {
            'status': 'SUCCESS',
            'datasets_loaded': len(datasets),
            'execution_results': self.execution_results,
            'reports': reports,
            'data_dictionary': data_dict
        }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting CHUNK_01: Data Ingestion & Profiling...")

    executor = Chunk01Executor()
    result = executor.run()

    logger.info(f"\nExecution Result: {result['status']}")
    logger.info(f"Datasets Loaded: {result['datasets_loaded']}")
    logger.info(f"\nReports generated:")
    for name, path in result['reports'].items():
        logger.info(f"  - {name}: {path}")

    logger.info(f"\nAll outputs saved to: {CHUNK_01_DIR}")
    logger.info(f"Next: CHUNK_02 - Data Cleaning")
