#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CHUNK_00: PROJECT SETUP - CROSS-PLATFORM RUNNER v2.0
================================================================================

UTF-8 Fixed Version - Works on Windows, Linux, and macOS

Usage:
    python RUN_CHUNK_00.py

================================================================================
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("\n" + "=" * 80)
    print(" PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS")
    print(" CHUNK_00: PROJECT SETUP AND INITIALIZATION (v2.0)")
    print("=" * 80 + "\n")

    current_dir = Path(__file__).parent
    script_path = current_dir / "scripts" / "CHUNK_00_PROJECT_SETUP_v2.py"

    if not script_path.exists():
        print(f"ERROR: Script not found at {script_path}")
        print(f"Please ensure CHUNK_00_PROJECT_SETUP_v2.py exists in the scripts/ directory")
        return 1

    print(f"Project Root: {current_dir.parent}")
    print(f"Running: {script_path}\n")

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(current_dir),
            check=False
        )

        if result.returncode == 0:
            print("\n" + "=" * 80)
            print(" CHUNK_00 EXECUTION COMPLETE")
            print("=" * 80 + "\n")
            print("Next steps:")
            print("  1. Review: documentation/CHUNK_00_EXECUTION_REPORT.md")
            print("  2. Check: config/ (5 JSON files)")
            print("  3. Review: logs/project_initialization.log")
            print("  4. Schedule: Sprint Planning Meeting for Day 2\n")
            print("Ready to proceed to CHUNK_01 upon executive sign-off.\n")
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
