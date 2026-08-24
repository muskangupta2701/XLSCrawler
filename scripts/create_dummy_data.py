import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_dummy_data(output_path="data/business_metrics.xlsx"):
    """Generates 30 days of business metrics with an anomaly on the last day."""
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Generate 30 days of dates
    end_date = datetime.now()
    dates = [(end_date - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(30)]
    dates.reverse() # Oldest to newest
    
    # Generate normal baseline data for the first 29 days
    revenue = np.random.normal(loc=5000, scale=200, size=29).tolist()
    orders = np.random.normal(loc=100, scale=5, size=29).tolist()
    conversion_rate = np.random.normal(loc=0.03, scale=0.002, size=29).tolist()
    traffic = np.random.normal(loc=3300, scale=150, size=29).tolist()
    cost = np.random.normal(loc=1500, scale=100, size=29).tolist()
    
    # Inject an anomaly on the 30th day (e.g., massive spike in traffic, drop in conversion, revenue steady)
    revenue.append(5100)           # Normal
    orders.append(105)             # Normal
    conversion_rate.append(0.015)  # ANOMALY: Drop! (Normal is ~0.03)
    traffic.append(7000)           # ANOMALY: Spike! (Normal is ~3300)
    cost.append(1600)              # Normal
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Revenue': revenue,
        'Orders': orders,
        'Conversion Rate': conversion_rate,
        'Traffic': traffic,
        'Cost': cost
    })
    
    # Save to Excel
    df.to_excel(output_path, index=False)
    print(f"Dummy data generated at {output_path}")
    print("Injected Anomaly on the last day: Traffic spiked, Conversion Rate dropped.")

if __name__ == "__main__":
    generate_dummy_data()
