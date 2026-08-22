@echo off
REM ============================================================================
REM CHUNK_01: DATA INGESTION & PROFILING - BATCH RUNNER
REM ============================================================================
REM Integrates all 8 CSV datasets and generates data profiles

echo.
echo ================================================================================
echo  PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
echo  CHUNK_01: DATA INGESTION AND PROFILING
echo ================================================================================
echo.

cd /d "%~dp0"

echo Project Root: %CD%\..
echo Data Root: C:\Users\rnand\OneDrive\Desktop^(1^)\home-credit-default-risk\data
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please ensure Python 3.8+ is installed.
    echo.
    pause
    exit /b 1
)

echo Python found. Running CHUNK_01_DATA_INGESTION.py...
echo.
echo This will:
echo   1. Load all 8 CSV datasets (1.4 GB)
echo   2. Validate data quality
echo   3. Profile data characteristics
echo   4. Generate data dictionary
echo   5. Create quality reports
echo.

python scripts\CHUNK_01_DATA_INGESTION.py

if errorlevel 1 (
    echo.
    echo ERROR: Script execution failed!
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ================================================================================
    echo  CHUNK_01 EXECUTION COMPLETE
    echo ================================================================================
    echo.
    echo Generated outputs:
    echo   - documentation/INGESTION_SUMMARY.txt
    echo   - documentation/DATA_QUALITY_REPORT.txt
    echo   - documentation/CHUNK_01_DETAILED_REPORT.md
    echo   - config/data_dictionary.json
    echo   - logs/chunk_01_execution.log
    echo.
    echo Available Library Functions:
    echo   - DataLoader: Load CSV files
    echo   - DataValidator: Check data quality
    echo   - DataProfiler: Profile data characteristics
    echo   - DataQualityReporter: Generate reports
    echo.
    echo Ready to proceed to CHUNK_02 - Data Cleaning
    echo.
)

pause
