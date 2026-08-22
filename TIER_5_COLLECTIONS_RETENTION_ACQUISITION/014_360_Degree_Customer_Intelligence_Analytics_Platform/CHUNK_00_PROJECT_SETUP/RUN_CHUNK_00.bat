@echo off
REM ============================================================================
REM CHUNK_00: PROJECT SETUP - BATCH RUNNER v2.0
REM ============================================================================
REM UTF-8 Fixed Version

echo.
echo ================================================================================
echo  PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
echo  CHUNK_00: PROJECT SETUP AND INITIALIZATION
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

echo Python found. Running CHUNK_00_PROJECT_SETUP_v2.py...
echo.

python scripts\CHUNK_00_PROJECT_SETUP_v2.py

if errorlevel 1 (
    echo.
    echo ERROR: Script execution failed!
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ================================================================================
    echo  CHUNK_00 EXECUTION COMPLETE
    echo ================================================================================
    echo.
    echo Next steps:
    echo   1. Review: documentation/CHUNK_00_EXECUTION_REPORT.md
    echo   2. Check: config/ (5 JSON files)
    echo   3. Review: logs/project_initialization.log
    echo   4. Schedule: Sprint Planning Meeting for Day 2
    echo.
    echo Ready to proceed to CHUNK_01 upon executive sign-off.
    echo.
)

pause
