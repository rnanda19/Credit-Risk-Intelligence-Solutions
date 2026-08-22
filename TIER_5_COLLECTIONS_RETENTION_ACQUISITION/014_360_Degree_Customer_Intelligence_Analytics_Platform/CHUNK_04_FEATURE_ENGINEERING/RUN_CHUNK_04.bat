@echo off
REM ============================================================================
REM CHUNK_04: FEATURE ENGINEERING - BATCH RUNNER
REM ============================================================================
REM Creates new features, encodes categoricals, scales, and selects features

echo.
echo ================================================================================
echo  PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
echo  CHUNK_04: FEATURE ENGINEERING
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

echo Python found. Running CHUNK_04_COMPLETE.py...
echo.
echo This will:
echo   1. Encode categorical variables
echo   2. Create polynomial and ratio features
echo   3. Scale and transform features
echo   4. Select high-variance features
echo   5. Detect redundant features
echo   6. Generate engineering reports
echo.

python scripts\CHUNK_04_COMPLETE.py

if errorlevel 1 (
    echo.
    echo ERROR: Script execution failed!
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ================================================================================
    echo  CHUNK_04 EXECUTION COMPLETE
    echo ================================================================================
    echo.
    echo Generated outputs:
    echo   - Engineered datasets
    echo   - Feature creation summary
    echo   - Feature selection results
    echo   - Quality assessment metrics
    echo.
    echo Available Library Functions:
    echo   - FeatureCreator: Create polynomial, interaction, ratio features
    echo   - CategoricalEncoder: Label encode, one-hot encode
    echo   - FeatureTransformer: Standardize, normalize features
    echo   - FeatureSelector: Select by variance, correlation
    echo   - FeatureQualityAssessor: Assess and detect redundancy
    echo.
    echo Ready to proceed to CHUNK_05 - Model Selection
    echo.
)

pause
