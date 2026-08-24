import pandas as pd
import os

def load_and_clean_data(file_path):
    """
    Reads the Excel file and performs basic data cleaning.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at {file_path}")
    
    print(f"Loading data from {file_path}...")
    df = pd.read_excel(file_path)
    
    # Basic cleaning
    # Forward-fill any missing values (assuming time-series continuity)
    df.ffill(inplace=True)
    
    # Ensure Date is datetime type
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        # Sort by date just to be safe
        df.sort_values(by='Date', inplace=True)
        df.reset_index(drop=True, inplace=True)
        
    return df
