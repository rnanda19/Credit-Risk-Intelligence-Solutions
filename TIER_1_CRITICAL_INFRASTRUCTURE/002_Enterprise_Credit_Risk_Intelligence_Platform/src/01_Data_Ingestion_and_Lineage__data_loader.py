
import logging
from pathlib import Path
import polars as pl
import sys
import numpy as np
sys.path.append(r"C:\Users\rnand\Documents\home-credit-default-risk\Enterprise_AI_Workflows\001_PD_Ultimate_Final")
from config import DATA_RAW_DIR, DATA_PROCESSED_DIR, LOGS_DIR

logging.basicConfig(filename=LOGS_DIR / "data_loader.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - [DataLoader] - %(message)s')

def ingest_all_datasets() -> None:
    print("Executing Data Ingestion Pipeline...")
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    raw_app_path = DATA_RAW_DIR / "application_train.csv"
    processed_app_path = DATA_PROCESSED_DIR / "master_features_engineered.parquet"

    if raw_app_path.exists():
        if not processed_app_path.exists():
            print(f"Converting {raw_app_path.name} to Parquet format...")
            df = pl.read_csv(raw_app_path)
            if "CREDIT_INCOME_RATIO" not in df.columns:
                df = df.with_columns((pl.col("AMT_CREDIT") / pl.col("AMT_INCOME_TOTAL")).alias("CREDIT_INCOME_RATIO"))
            df.write_parquet(processed_app_path)
            print(f"[SUCCESS] Saved processed features to {processed_app_path}")
        else:
            print("[SUCCESS] Processed features already exist.")
    else:
        print("[WARNING] Raw file not found. Creating a synthetic mockup dataset for testing workflow execution...")
        np.random.seed(42)
        n = 1000
        df = pl.DataFrame({
            "SK_ID_CURR": range(100000, 100000 + n),
            "TARGET": np.random.choice([0, 1], size=n, p=[0.9, 0.1]),
            "AMT_INCOME_TOTAL": np.random.uniform(30000, 300000, n),
            "AMT_CREDIT": np.random.uniform(100000, 1500000, n),
            "AMT_ANNUITY": np.random.uniform(5000, 50000, n),
            "DAYS_BIRTH": np.random.randint(-25000, -20000, n),
            "DAYS_EMPLOYED": np.random.randint(-5000, -100, n),
            "CREDIT_INCOME_RATIO": np.random.uniform(1, 10, n)
        })
        df.write_parquet(processed_app_path)
        print("[SUCCESS] Synthetic test dataset created successfully.")
