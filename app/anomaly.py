from sklearn.ensemble import IsolationForest
import joblib
from pathlib import Path

MODEL_PATH = Path("models/anomaly_detector.pkl")

def detect_anomalies(df):
    features = ["data_used_gb","calls_duration_min","bill_amount"]
    model = IsolationForest(contamination=0.05, random_state=42)
    df["anomaly"] = model.fit_predict(df[features])
    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return df
