def print_recommendations(df, n=5):
    for _, row in df.head(n).iterrows():
        print(f"User: {row['user_id']}")
        print(f"Current Plan: {row['plan_name']}")
        print(f"Avg Data Usage: {row['data_used_gb']:.2f} GB/month")
        print(f"Recommended Plan: {row['recommended_plan']}")
        print("-" * 40)
