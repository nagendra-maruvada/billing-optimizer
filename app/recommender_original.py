PLANS = [
    {"name": "Month-to-month", "limit_gb": 10, "price": 70},
    {"name": "One year", "limit_gb": 20, "price": 60},
    {"name": "Two year", "limit_gb": 30, "price": 50},
]

def recommend_plan(avg_usage):
    for p in PLANS:
        if avg_usage <= p["limit_gb"]:
            return p["name"]
    return "Two year"

def build_recommendations(df):
    summary = df.groupby("user_id").agg({
        "data_used_gb": "mean",
        "calls_duration_min": "mean",
        "bill_amount": "mean",
        "plan_name": "first"
    }).reset_index()

    summary["recommended_plan"] = summary["data_used_gb"].apply(recommend_plan)
    return summary
