import pandas as pd
from .config import BASELINE_DAYS, ANOMALY_THRESHOLD_PCT

def detect_anomalies(df):
    """
    Checks the latest day's data against the rolling baseline.
    Returns a dictionary of anomalies if found.
    """
    if len(df) < BASELINE_DAYS + 1:
        print("Not enough data to calculate baselines.")
        return {}

    metrics_to_check = [col for col in df.columns if col != 'Date']
    
    # Get the latest row
    latest_date = df['Date'].iloc[-1]
    latest_data = df.iloc[-1]
    
    # Get the baseline (average of the previous BASELINE_DAYS days)
    # We exclude the latest day from the baseline calculation
    baseline_data = df.iloc[-(BASELINE_DAYS+1):-1][metrics_to_check].mean()
    
    anomalies = {}
    
    print(f"Checking data for {latest_date.strftime('%Y-%m-%d')} against {BASELINE_DAYS}-day baseline...")
    
    for metric in metrics_to_check:
        current_value = latest_data[metric]
        baseline_value = baseline_data[metric]
        
        # Avoid division by zero
        if baseline_value == 0:
            continue
            
        pct_change = (current_value - baseline_value) / baseline_value
        
        # Check if the absolute percentage change exceeds the threshold
        if abs(pct_change) > ANOMALY_THRESHOLD_PCT:
            direction = "increased" if pct_change > 0 else "decreased"
            anomalies[metric] = {
                "current": current_value,
                "baseline": baseline_value,
                "pct_change": pct_change,
                "direction": direction
            }
            print(f"! Anomaly detected in {metric}: {direction} by {pct_change:.1%}")
            
    return {
        "date": latest_date.strftime('%Y-%m-%d'),
        "anomalies": anomalies
    }
