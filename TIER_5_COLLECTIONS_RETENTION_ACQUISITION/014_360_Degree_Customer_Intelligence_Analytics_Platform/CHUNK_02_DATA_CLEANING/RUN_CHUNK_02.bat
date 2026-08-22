@echo off
REM ============================================================================
REM CHUNK_02: DATA CLEANING & PREPROCESSING - BATCH RUNNER
REM ============================================================================
REM Cleans and preprocesses data from CHUNK_01

echo.
echo ================================================================================
echo  PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
echo  CHUNK_02: DATA CLEANING AND PREPROCESSING
echo ================================================================================
echo.

cd /d "%~dp0"

echo Project Root: %CD%\..
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please ensure Python 3.8+ is installed.
    echo.
    pause
    exit /b 1
)

echo Python found. Running CHUNK_02_INTERACTIVE.py...
echo.
echo This will:
echo   1. Load cleaned datasets from CHUNK_01
echo   2. Handle missing values
echo   3. Remove duplicate records
echo   4. Validate data quality
echo   5. Generate cleaning reports
echo.

python scripts\CHUNK_02_INTERACTIVE.py

if errorlevel 1 (
    echo.
    echo ERROR: Script execution failed!
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ================================================================================
    echo  CHUNK_02 EXECUTION COMPLETE
    echo ================================================================================
    echo.
    echo Generated outputs:
    echo   - documentation/CHUNK_02_CLEANING_SUMMARY.txt
    echo   - config/chunk_02_metadata.json
    echo   - logs/chunk_02_execution.log
    echo.
    echo Available Library Functions:
    echo   - MissingValueHandler: Handle missing data
    echo   - DuplicateHandler: Remove duplicates
    echo   - OutlierHandler: Detect and treat outliers
    echo   - DataTypeConverter: Optimize data types
    echo   - CategoricalEncoder: Encode categories
    echo   - DataQualityValidator: Validate cleaned data
    echo.
    echo Ready to proceed to CHUNK_03 - Feature Validation
    echo.
)

pause
