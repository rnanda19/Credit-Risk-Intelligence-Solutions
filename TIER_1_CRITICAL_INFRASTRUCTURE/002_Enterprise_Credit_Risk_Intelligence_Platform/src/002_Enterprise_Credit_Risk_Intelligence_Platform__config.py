
from pathlib import Path
BASE_DIR = Path(r"C:\Users\rnand\Documents\home-credit-default-risk\Enterprise_AI_Workflows\001_PD_Ultimate_Final")
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"
RANDOM_STATE = 42
TARGET_COL = "TARGET"
ID_COL = "SK_ID_CURR"
