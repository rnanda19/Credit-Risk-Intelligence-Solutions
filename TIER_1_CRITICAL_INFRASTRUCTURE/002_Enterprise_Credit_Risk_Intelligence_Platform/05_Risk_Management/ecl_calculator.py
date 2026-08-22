
import pickle
import logging
from pathlib import Path
import polars as pl
import sys
sys.path.append(r"C:\Users\rnand:\Documents\home-credit-default-risk\Enterprise_AI_Workflows\001_PD_Ultimate_Final")
from config import DATA_PROCESSED_DIR, MODELS_DIR, ID_COL

def calculate_portfolio_ecl():
    print("Executing Enterprise ECL (Expected Credit Loss) Engine...")
    feature_path = DATA_PROCESSED_DIR / "master_features_engineered.parquet"
    champion_path = MODELS_DIR / "champion_pd_model.pkl"

    df = pl.read_parquet(feature_path)
    with open(champion_path, "rb") as f:
        model = pickle.load(f)

    numeric_features = [col for col in df.columns if col not in [ID_COL, 'TARGET'] and df[col].dtype in [pl.Float32, pl.Float64, pl.Int32, pl.Int64]]
    X = df.select(numeric_features).fill_null(0).to_numpy()

    df = df.with_columns(pl.Series("PD", model.predict_proba(X)[:, 1]))
    LGD = 0.90
    df = df.with_columns((pl.col("PD") * LGD * pl.col("AMT_CREDIT")).alias("ECL_AMOUNT"))

    total_ecl = df.select(pl.col("ECL_AMOUNT").sum()).item()
    print(f"==================================================")
    print(f"[SUCCESS] Portfolio Provisioning Calculation Complete")
    print(f"Total Expected Credit Loss (ECL): ${total_ecl:,.2f}")
    print(f"==================================================")
