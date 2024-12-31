import os
import pandas as pd

# ------------------------------------------------------------------------
# 1) Define Paths
# ------------------------------------------------------------------------

# Dynamically determine the project root based on this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))  # Adjust if your structure differs

# Path to the tickers.txt file
TICKERS_FILE = os.path.join(PROJECT_ROOT, "tickers.txt")  # Adjust if tickers.txt is located elsewhere

# Directory containing the raw stock CSVs
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "stock_data")

# Directory to save the processed CSVs
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "formatted", "stocks")
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# ------------------------------------------------------------------------
# 2) Read Tickers
# ------------------------------------------------------------------------

def load_tickers(ticker_file):
    """
    Reads ticker symbols (one per line) from a text file.
    Returns a list of ticker strings.
    """
    if not os.path.exists(ticker_file):
        raise FileNotFoundError(f"Ticker file not found at: {ticker_file}")
    
    with open(ticker_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Replace '.' with '-' for Yahoo Finance compatibility (e.g., BRK.B -> BRK-B)
    tickers = [line.strip().replace('.', '-') for line in lines if line.strip()]
    return tickers

# ------------------------------------------------------------------------
# 3) Format CSV Function
# ------------------------------------------------------------------------

def format_csv(ticker, raw_dir, processed_dir):
    """
    Reads a CSV file for a given ticker, converts the 'Date' column to pd.DateTime,
    and saves the formatted DataFrame to the processed directory.
    """
    raw_csv_path = os.path.join(raw_dir, f"{ticker}.csv")
    
    if not os.path.exists(raw_csv_path):
        print(f"Warning: CSV for ticker '{ticker}' not found at {raw_csv_path}. Skipping.")
        return None
    
    try:
        # Read the CSV into a DataFrame
        df = pd.read_csv(raw_csv_path)
        
        # Check if 'Date' column exists
        if "Date" not in df.columns:
            raise ValueError(f"'Date' column not found in {raw_csv_path}.")
        
        # Convert 'Date' to datetime
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        
        # Handle rows where 'Date' conversion failed
        if df["Date"].isnull().any():
            num_invalid = df["Date"].isnull().sum()
            print(f"Warning: {num_invalid} invalid dates found in {raw_csv_path}. These rows will be dropped.")
            df = df.dropna(subset=["Date"])
        
        # Optional: Sort by Date
        df = df.sort_values("Date")
        
        # Optional: Reset index
        df = df.reset_index(drop=True)
        
        # Save the formatted DataFrame to the processed directory
        processed_csv_path = os.path.join(processed_dir, f"{ticker}.csv")
        df.to_csv(processed_csv_path, index=False)
        
        print(f"Formatted and saved: {processed_csv_path}")
        return df  # Optionally return the DataFrame if needed elsewhere
    
    except Exception as e:
        print(f"Error processing {raw_csv_path}: {e}")
        return None

# ------------------------------------------------------------------------
# 4) Main Formatting Process
# ------------------------------------------------------------------------

def get_formatted_data():
    """
    Reads all tickers from tickers.txt, formats their CSVs,
    saves the formatted CSVs, and returns a dictionary of DataFrames
    keyed by ticker symbol.
    """
    # Load all tickers
    try:
        tickers = load_tickers(TICKERS_FILE)
        print(f"Loaded {len(tickers)} tickers from '{TICKERS_FILE}'.")
    except Exception as e:
        print(f"Error loading tickers: {e}")
        return {}
    
    # Initialize dictionary to hold DataFrames
    data = {}
    
    # Iterate through each ticker and format its CSV
    for ticker in tickers:
        df = format_csv(ticker, RAW_DATA_DIR, PROCESSED_DATA_DIR)
        if df is not None:
            data[ticker] = df
    
    print("All tickers have been processed.")
    return data

# ------------------------------------------------------------------------
# 5) Execute the Script (Optional)
# ------------------------------------------------------------------------

if __name__ == "__main__":
    formatted_data = get_formatted_data()
    print(type(formatted_data))
    
    # Example: Accessing a specific ticker's DataFrame
    example_ticker = "AAPL"
    if example_ticker in formatted_data:
        print(f"\nFirst 5 rows for {example_ticker}:")
        print(formatted_data[example_ticker].head())
    else:
        print(f"{example_ticker} not found in the formatted data.")
