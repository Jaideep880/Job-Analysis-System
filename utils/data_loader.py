import pandas as pd
from pathlib import Path

def load_data(file_path=None):
    """
    Load and process job market data.
    
    Args:
        file_path (str, optional): Path to the data file. If None, uses default path.
    
    Returns:
        pd.DataFrame: Processed job market data
    """
    try:
        if file_path is None:
            # Use default data path
            file_path = Path(__file__).parent.parent / 'data' / 'processed' / 'job_market_data.csv'
        
        if not file_path.exists():
            print(f"Data file not found at {file_path}")
            return pd.DataFrame()
        
        df = pd.read_csv(file_path)
        
        if df.empty:
            print("Loaded data is empty")
            return df
        
        # Convert published_date to datetime
        if 'published_date' in df.columns:
            df['published_date'] = pd.to_datetime(df['published_date']).dt.tz_localize(None)
        else:
            print("Warning: 'published_date' column not found in data")
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame() 