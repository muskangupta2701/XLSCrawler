import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Anomaly Detection Settings
# If a metric changes by more than this percentage compared to the baseline, it's an anomaly.
ANOMALY_THRESHOLD_PCT = 0.20 
# Number of days to use for calculating the moving average baseline
BASELINE_DAYS = 7 

# Email Settings
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
