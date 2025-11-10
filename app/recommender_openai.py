from openai import OpenAI
import os
import pandas as pd

# Initialize OpenAI client (reads OPENAI_API_KEY from env)
client = OpenAI(api_key="")

PLANS = [
    {"name": "Month-to-month", "limit_gb": 10, "price": 70},
    {"name": "One year", "limit_gb": 20, "price": 60},
    {"name": "Two year", "limit_gb": 30, "price": 50},
]

def ai_recommend_plan(avg_usage, current_plan, avg_bill):
    """
    Use ChatGPT API to generate an AI-based plan recommendation.
    """
    prompt = (
        f"You are a telecom billing assistant. "
        f"The user currently has a '{current_plan}' plan, spends around ₹{avg_bill:.0f} per month, "
        f"and uses {avg_usage:.1f} GB of data monthly. "
        "Given the available plans: Month-to-month, One year, and Two year — "
        "suggest the most cost-effective plan and explain briefly why."
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",   # fast and affordable ChatGPT model
            messages=[
                {"role": "system", "content": "You are an expert telecom plan optimizer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=80,
            temperature=0.6,
        )

        reply = completion.choices[0].message.content
        # Try to detect which plan was mentioned
        for plan in [p["name"] for p in PLANS]:
            if plan.lower() in reply.lower():
                return plan
        return "One year"
    except Exception as e:
        print("⚠️ OpenAI API error:", e)
        # Fallback rule
        if avg_usage <= 10:
            return "Month-to-month"
        elif avg_usage <= 20:
            return "One year"
        return "Two year"


def build_recommendations(df):
    """
    Build AI-powered personalized plan recommendations using ChatGPT.
    """
    summary = df.groupby("user_id").agg({
        "data_used_gb": "mean",
        "calls_duration_min": "mean",
        "bill_amount": "mean",
        "plan_name": "first"
    }).reset_index()

    print("🤖 Fetching recommendations from ChatGPT...")
    summary["recommended_plan"] = summary.apply(
        lambda r: ai_recommend_plan(
            r["data_used_gb"],
            r["plan_name"],
            r["bill_amount"]
        ),
        axis=1
    )

    return summary
