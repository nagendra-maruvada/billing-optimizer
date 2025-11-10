# AI-Powered Billing Optimization (Local MVP)

This is a local MVP that:
- Loads real telecom billing data (from Kaggle Telco Churn dataset)
- Detects billing anomalies
- Suggests optimal plans
- Generates AI-based summaries

Key Features:
 1. Anomaly Detection:
    - Identifies unusual usage patterns
    - Uses machine learning (Isolation Forest)
    - Configurable sensitivity (5% anomaly rate)
 2. Plan Optimization:
    - Data usage analysis
    - Cost optimization
    - Multiple recommendation strategies (rule-based and AI)
 3. AI Integration:
    - Multiple AI backends supported
    - Natural language summaries
    - Extensible architecture
 4. Data Processing:
    - Handles real telecom data
    - Synthetic data generation for testing
    - Robust error handling

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
