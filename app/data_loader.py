import pandas as pd
import numpy as np
from pathlib import Path
from .anomaly import detect_anomalies
from datetime import datetime

def load_and_prepare_data():
    data_path = Path("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    if not data_path.exists():
        raise FileNotFoundError("Please place the Kaggle dataset in the data/ folder")

    df = pd.read_csv(data_path)

    # create a synthetic 'date' by adding tenure (in months) to a baseline date
    start = pd.to_datetime("2025-01-01")
    df["tenure"] = pd.to_numeric(df.get("tenure", 0), errors="coerce").fillna(0).astype(int)
    df["date"] = df["tenure"].apply(lambda m: start + pd.DateOffset(months=int(m)))

    # Set random seed for reproducibility
    np.random.seed(42)

    # Generate normal usage patterns
    df["data_used_gb"] = np.where(df["InternetService"] == "Fiber optic",
                                 np.random.normal(15, 5, len(df)),
                                 np.random.normal(5, 2, len(df)))
    df["calls_duration_min"] = np.random.normal(200, 50, len(df))
    df["bill_amount"] = df["MonthlyCharges"]

    # Introduce anomalies for 2-3% of users, focusing on recent months
    current_date = pd.to_datetime("2025-11-09")  # Current date
    recent_mask = (current_date - df["date"]).dt.days <= 30  # Last 30 days
    recent_users = df[recent_mask].index
    num_anomalies = int(len(recent_users) * 0.025)  # 2.5% of recent users
    anomaly_indices = np.random.choice(recent_users, size=num_anomalies, replace=False)

    # Create extreme spikes in usage and billing
    df.loc[anomaly_indices, "data_used_gb"] *= np.random.uniform(8, 10, size=len(anomaly_indices))  # 8-10x normal usage
    df.loc[anomaly_indices, "calls_duration_min"] *= np.random.uniform(5, 7, size=len(anomaly_indices))  # 5-7x normal calls
    df.loc[anomaly_indices, "bill_amount"] *= np.random.uniform(6, 8, size=len(anomaly_indices))  # 6-8x normal bill

    df["plan_name"] = df["Contract"]

    df = df[["customerID", "date", "data_used_gb", "calls_duration_min", "bill_amount", "plan_name"]]
    df.rename(columns={"customerID": "user_id"}, inplace=True)

    # Apply anomaly detection
    df = detect_anomalies(df)

    # Convert anomaly labels (-1 for anomalies, 1 for normal) to boolean (True for anomalies)
    df["is_anomaly"] = df["anomaly"].apply(lambda x: x == -1)

    # Drop the intermediate anomaly column
    df = df.drop("anomaly", axis=1)

    return df
