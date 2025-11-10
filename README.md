# AI-Powered Billing Optimization (Local MVP)

This is a local MVP that:
- Loads real telecom billing data (from Kaggle Telco Churn dataset)
- Detects billing anomalies
- Suggests optimal plans
- Generates AI-based summaries

## Usage
1. Place `WA_Fn-UseC_-Telco-Customer-Churn.csv` into the `data/` folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the main app:
   ```bash
   python app/main.py
   ```
## Outcome
python run_main_wrapper.py
Device set to use cpu
✅ Using Groq Cloud model: openai/gpt-oss-20b
📊 Loading and preparing real telecom data...

🚨 Top 5 Most Significant Anomalies:

Found 1 total anomalies. Showing top 5 most severe cases:

🚨 #7 SEVERE ANOMALY - User 1452-KIOVK:
  📱 Data Usage: 22.9 GB
  ⏱️ Call Duration: 142.5 minutes
  💰 Bill Amount: $89.10
  📅 Date: 2026-11-01
  📊 Above Average: Data: 0%, Calls: 0%, Bill: 0%

🤖 Building personalized recommendations...
🤖 Building AI-driven personalized recommendations...
User: 0002-ORFBO
Current Plan: One year
Avg Data Usage: 2.18 GB/month
Recommended Plan: One year
----------------------------------------
User: 0003-MKNFE
Current Plan: Month-to-month
Avg Data Usage: 3.18 GB/month
Recommended Plan: One year
----------------------------------------
User: 1452-KIOVK
Current Plan: Month-to-month
Avg Data Usage: 22.90 GB/month
Recommended Plan: One year
----------------------------------------
User: 3668-QPYBK
Current Plan: Month-to-month
Avg Data Usage: 5.48 GB/month
Recommended Plan: One year
----------------------------------------
User: 5575-GNVDE
Current Plan: One year
Avg Data Usage: 4.07 GB/month
Recommended Plan: One year
----------------------------------------

<img width="1314" height="549" alt="image" src="https://github.com/user-attachments/assets/80b87f70-e624-48ba-853a-3be33195e8b2" />
