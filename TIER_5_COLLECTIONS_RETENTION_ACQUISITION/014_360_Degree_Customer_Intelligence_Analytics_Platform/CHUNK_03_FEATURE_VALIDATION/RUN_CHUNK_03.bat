@echo off
REM ============================================================================
REM CHUNK_03: FEATURE VALIDATION & EXPLORATION - BATCH RUNNER
REM ============================================================================
REM Validates and explores features from cleaned datasets

echo.
echo ================================================================================
echo  PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
echo  CHUNK_03: FEATURE VALIDATION AND EXPLORATION
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

echo Python found. Running CHUNK_03_INTERACTIVE.py...
echo.
echo This will:
echo   1. Load cleaned datasets from CHUNK_02
echo   2. Analyze feature distributions
echo   3. Compute correlations
echo   4. Assess feature quality
echo   5. Validate statistical properties
echo   6. Generate exploration reports
echo.

python scripts\CHUNK_03_INTERACTIVE.py

if errorlevel 1 (
    echo.
    echo ERROR: Script execution failed!
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ================================================================================
    echo  CHUNK_03 EXECUTION COMPLETE
    echo ================================================================================
    echo.
    echo Generated outputs:
    echo   - documentation/CHUNK_03_EXPLORATION_SUMMARY.txt
    echo   - config/chunk_03_metadata.json
    echo   - logs/chunk_03_execution.log
    echo.
    echo Available Library Functions:
    echo   - FeatureDistributionAnalyzer: Analyze distributions
    echo   - CorrelationAnalyzer: Compute correlations
    echo   - FeatureQualityAssessor: Assess quality
    echo   - StatisticalValidator: Validate statistically
    echo   - ExplorationReportGenerator: Generate reports
    echo.
    echo Ready to proceed to CHUNK_04 - Feature Engineering
    echo.
)

pause
