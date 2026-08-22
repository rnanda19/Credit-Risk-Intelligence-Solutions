@echo off
REM ============================================================================
REM CHUNK_05: MODEL SELECTION & TRAINING - BATCH RUNNER
REM ============================================================================
REM Trains multiple ML models with cross-validation and evaluation

echo.
echo ================================================================================
echo  PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
echo  CHUNK_05: MODEL SELECTION AND TRAINING
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

echo Python found. Running CHUNK_05_COMPLETE.py...
echo.
echo This will:
echo   1. Select optimal ML algorithms
echo   2. Prepare data for model training
echo   3. Train models with 5-fold cross-validation
echo   4. Evaluate model performance (accuracy, precision, recall, F1)
echo   5. Analyze feature importance
echo   6. Compare and rank models
echo   7. Identify best performing model
echo.

python scripts\CHUNK_05_COMPLETE.py

if errorlevel 1 (
    echo.
    echo ERROR: Script execution failed!
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ================================================================================
    echo  CHUNK_05 EXECUTION COMPLETE
    echo ================================================================================
    echo.
    echo Generated outputs:
    echo   - Trained models (4 different algorithms)
    echo   - Cross-validation scores
    echo   - Performance metrics per model
    echo   - Feature importance rankings
    echo   - Best model identification
    echo.
    echo Available Library Functions:
    echo   - ModelSelector: Select algorithms for problem type
    echo   - ModelTrainer: Train models with cross-validation
    echo   - ModelEvaluator: Calculate performance metrics
    echo   - FeatureImportanceAnalyzer: Extract feature rankings
    echo   - HyperparameterTuner: Grid and random search
    echo   - ModelComparator: Compare and rank models
    echo.
    echo Ready to proceed to CHUNK_06 - Model Validation
    echo.
)

pause
