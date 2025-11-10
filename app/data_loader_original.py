import pandas as pd
import numpy as np
from pathlib import Path

def load_and_prepare_data():
    data_path = Path("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    if not data_path.exists():
        raise FileNotFoundError("Please place the Kaggle dataset in the data/ folder")

    df = pd.read_csv(data_path)

    # create a synthetic 'date' by adding tenure (in months) to a baseline date
    start = pd.to_datetime("2025-01-01")
    # tenure is in months — pandas doesn't allow unit='M' for to_timedelta, so use DateOffset per row
    df["tenure"] = pd.to_numeric(df.get("tenure", 0), errors="coerce").fillna(0).astype(int)
    df["date"] = df["tenure"].apply(lambda m: start + pd.DateOffset(months=int(m)))

    np.random.seed(42)
    df["data_used_gb"] = np.where(df["InternetService"] == "Fiber optic",
                                  np.random.normal(15, 5, len(df)),
                                  np.random.normal(5, 2, len(df)))
    df["calls_duration_min"] = np.random.normal(200, 50, len(df))
    df["bill_amount"] = df["MonthlyCharges"]
    df["plan_name"] = df["Contract"]

    df = df[["customerID","date","data_used_gb","calls_duration_min","bill_amount","plan_name"]]
    df.rename(columns={"customerID":"user_id"}, inplace=True)

    return df
