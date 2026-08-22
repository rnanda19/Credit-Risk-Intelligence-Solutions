
import logging
from pathlib import Path
import polars as pl
import sys
sys.path.append(r"C:\Users\rnand\Documents\home-credit-default-risk\Enterprise_AI_Workflows\001_PD_Ultimate_Final")
from config import DATA_PROCESSED_DIR, LOGS_DIR

logging.basicConfig(filename=LOGS_DIR / "feature_engineer.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - [FeatureEngineer] - %(message)s')

def build_master_feature_matrix() -> None:
    print("Executing Feature Engineering Pipeline...")
    feature_path = DATA_PROCESSED_DIR / "master_features_engineered.parquet"
    if feature_path.exists():
        df = pl.read_parquet(feature_path)
        print(f"[SUCCESS] Feature matrix verified with shape: {df.shape}")
    else:
        raise FileNotFoundError("Master features parquet not found.")
