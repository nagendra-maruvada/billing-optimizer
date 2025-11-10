import os
import pandas as pd
from transformers import pipeline

# ✅ Always initialize a local fallback (fast, offline)
generator = pipeline("text-generation", model="distilgpt2")

# ✅ Groq configuration
GROQ_MODEL = "openai/gpt-oss-20b"
USE_GROQ = False
client = None

try:
    from groq import Groq
    GROQ_API_KEY = "abc"
    if GROQ_API_KEY:
        client = Groq(api_key=GROQ_API_KEY)
        USE_GROQ = True
        print(f"✅ Using Groq Cloud model: {GROQ_MODEL}")
    else:
        print("⚠️ GROQ_API_KEY not set. Using local model only.")
except Exception as e:
    print("⚠️ Groq client unavailable. Using local model only:", e)

# ✅ Example available plans
PLANS = [
    {"name": "Month-to-month", "limit_gb": 10, "price": 70},
    {"name": "One year", "limit_gb": 20, "price": 60},
    {"name": "Two year", "limit_gb": 30, "price": 50},
]


def ai_recommend_plan(avg_usage, current_plan, avg_bill):
    """
    Generate personalized plan recommendation using Groq or local model.
    """
    prompt = (
        f"You are a telecom billing optimizer.\n"
        f"User has '{current_plan}' plan, spends ₹{avg_bill:.0f}/month, "
        f"and uses {avg_usage:.1f} GB of data monthly.\n"
        "Available plans:\n"
        "1. Month-to-month — 10 GB ₹70\n"
        "2. One year — 20 GB ₹60\n"
        "3. Two year — 30 GB ₹50\n"
        "Pick the best value plan and explain briefly (max 1 line).\n"
        "Respond only in format: <Plan>: <Reason>"
    )

    # --- 1️⃣ Try Groq ---
    if USE_GROQ:
        try:
            completion = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert telecom billing assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=60,
                temperature=0.6,
            )
            reply = completion.choices[0].message.content.strip()
            for plan in [p["name"] for p in PLANS]:
                if plan.lower() in reply.lower():
                    return plan
            return "One year"
        except Exception as e:
            print("⚠️ Groq API error — using local fallback:", e)

    # --- 2️⃣ Local model fallback (distilgpt2) ---
    try:
        response = generator(
            prompt,
            max_new_tokens=25,
            truncation=True,
            pad_token_id=50256,
            num_return_sequences=1
        )
        text = response[0]["generated_text"]
        for plan in ["Month-to-month", "One year", "Two year"]:
            if plan.lower() in text.lower():
                return plan
    except Exception as e:
        print("⚠️ Local model error:", e)

    # --- 3️⃣ Rule-based backup ---
    if avg_usage <= 10:
        return "Month-to-month"
    elif avg_usage <= 20:
        return "One year"
    else:
        return "Two year"


def build_recommendations(df):
    """
    Build AI-driven personalized billing plan recommendations.
    """
    summary = df.groupby("user_id").agg({
        "data_used_gb": "mean",
        "calls_duration_min": "mean",
        "bill_amount": "mean",
        "plan_name": "first"
    }).reset_index()

    print("🤖 Building AI-driven personalized recommendations...")

    summary["recommended_plan"] = summary.apply(
        lambda r: ai_recommend_plan(
            r["data_used_gb"],
            r["plan_name"],
            r["bill_amount"]
        ),
        axis=1
    )

    return summary
