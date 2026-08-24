from src.data_loader import load_and_clean_data
from src.detector import detect_anomalies
from src.summarizer import generate_summary
from src.notifier import send_alert
import os

def run_watcher():
    """Main orchestration function."""
    print("Starting AI Anomaly Watcher...")
    
    data_file = "data/business_metrics.xlsx"
    
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found. Please run scripts/create_dummy_data.py first.")
        return

    # Step 1: Read Data
    df = load_and_clean_data(data_file)
    
    # Step 2: Detect Anomalies
    report = detect_anomalies(df)
    
    if report.get("anomalies"):
        # Step 3: Summarize via AI
        summary = generate_summary(report)
        
        # Step 4: Alert
        send_alert(report, summary)
    else:
        print("No significant anomalies detected today. All metrics within normal ranges.")
        
    print("Watcher finished.")

if __name__ == "__main__":
    run_watcher()
