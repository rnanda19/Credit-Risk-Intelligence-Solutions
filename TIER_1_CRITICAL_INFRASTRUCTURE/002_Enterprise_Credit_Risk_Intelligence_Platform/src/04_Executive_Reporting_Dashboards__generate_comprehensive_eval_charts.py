
import logging
from pathlib import Path
import sys
sys.path.append(r"C:\Users\rnand\Documents\home-credit-default-risk\Enterprise_AI_Workflows\001_PD_Ultimate_Final")
from config import REPORTS_DIR

def generate_comprehensive_evaluation_suite():
    print("Generating Evaluation Dashboards & Artifacts...")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[SUCCESS] Output reporting directory ready at {REPORTS_DIR}")
