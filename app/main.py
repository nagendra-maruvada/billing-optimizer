from app.data_loader import load_and_prepare_data
from app.recommender import build_recommendations
from app.utils import print_recommendations
import argparse


def main(allow_model_download: bool = False):
    print("📊 Loading and preparing real telecom data...")
    df = load_and_prepare_data()

    print("\n🚨 Top 5 Most Significant Anomalies:")
    anomalies = df[df["is_anomaly"]].copy()

    # Calculate a composite score for anomaly severity
    anomalies['severity_score'] = (
        (anomalies['data_used_gb'] / anomalies['data_used_gb'].mean()) +
        (anomalies['calls_duration_min'] / anomalies['calls_duration_min'].mean()) +
        (anomalies['bill_amount'] / anomalies['bill_amount'].mean())
    )

    # Sort by severity score and get top 5
    top_anomalies = anomalies.nlargest(5, 'severity_score')
    print(f"\nFound {len(anomalies)} total anomalies. Showing top 5 most severe cases:")

    for idx, row in top_anomalies.iterrows():
        print(f"\n🚨 #{idx + 1} SEVERE ANOMALY - User {row['user_id']}:")
        print(f"  📱 Data Usage: {row['data_used_gb']:.1f} GB")
        print(f"  ⏱️ Call Duration: {row['calls_duration_min']:.1f} minutes")
        print(f"  💰 Bill Amount: ${row['bill_amount']:.2f}")
        print(f"  📅 Date: {row['date'].strftime('%Y-%m-%d')}")
        # Calculate percentage above mean
        data_pct = ((row['data_used_gb'] / anomalies['data_used_gb'].mean()) - 1) * 100
        calls_pct = ((row['calls_duration_min'] / anomalies['calls_duration_min'].mean()) - 1) * 100
        bill_pct = ((row['bill_amount'] / anomalies['bill_amount'].mean()) - 1) * 100
        print(f"  📊 Above Average: Data: {data_pct:.0f}%, Calls: {calls_pct:.0f}%, Bill: {bill_pct:.0f}%")

    print("\n🤖 Building personalized recommendations...")
    summary = build_recommendations(df)

    print_recommendations(summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run billing-optimizer main pipeline")
    parser.add_argument("--download-model", action="store_true", help="Allow downloading transformer model if not found locally")
    args = parser.parse_args()
    main(allow_model_download=args.download_model)
