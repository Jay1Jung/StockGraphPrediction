import os
import pandas as pd
import yfinance as yf

def load_tickers(ticker_file):
    """
    Reads ticker symbols (one per line) from a text or CSV file.
    Returns a list of ticker strings.
    """
    with open(ticker_file, 'r') as f:
        lines = f.readlines()
    # Strip whitespace and ignore empty lines
    tickers = [line.strip() for line in lines if line.strip()]
    return tickers

def incremental_download(ticker, output_dir, start_date, end_date):
    """
    Incrementally download data for a single ticker from yfinance.
    If a CSV for this ticker already exists, only fetch *new* data from
    (last_date + 1 day) up to end_date. Then append to the existing CSV.
    """
    # 1) Determine CSV path for this ticker
    csv_path = os.path.join(output_dir, f"{ticker}.csv")
    
    # 2) Check if CSV already exists
    if os.path.exists(csv_path):
        # Load existing data
        existing_df = pd.read_csv(csv_path)
        
        # Make sure 'Date' is datetime
        if 'Date' in existing_df.columns:
            existing_df['Date'] = pd.to_datetime(existing_df['Date'])
        else:
            # If yfinance data is indexed by date, the column might be unnamed
            raise ValueError(f"Existing CSV for {ticker} has unexpected format.")

        # Find the last date in your existing data
        last_date = existing_df['Date'].max()
        
        # 3) Compute the new start date as last_date + 1 day
        new_start = last_date + pd.Timedelta(days=1)
        
        # If new_start is already beyond end_date, no need to download
        if new_start > pd.to_datetime(end_date):
            print(f"{ticker}: No new data to download. Skipping.")
            return
        
        # 4) Download only the new data
        print(f"{ticker}: Downloading from {new_start.date()} to {end_date}...")
        new_df = yf.download(ticker, start=new_start.strftime('%Y-%m-%d'), end=end_date)
        
        if new_df.empty:
            print(f"{ticker}: No new data returned by yfinance.")
            return
        
        # yfinance typically places dates in the index. Let's fix that:
        new_df.reset_index(inplace=True)
        new_df['Date'] = pd.to_datetime(new_df['Date'])
        
        # 5) Concatenate existing + new, remove duplicates
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df.drop_duplicates(subset=['Date'], keep='last', inplace=True)
        
        # 6) Save updated data
        combined_df.to_csv(csv_path, index=False)
        print(f"{ticker}: CSV updated with {len(new_df)} new rows.")
        
    else:
        # CSV doesn't exist -> fetch all data from start_date to end_date
        print(f"{ticker}: No existing CSV found. Downloading full history...")
        df = yf.download(ticker, start=start_date, end=end_date)
        
        if df.empty:
            print(f"{ticker}: No data returned by yfinance.")
            return
        
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Save to CSV
        df.to_csv(csv_path, index=False)
        print(f"{ticker}: CSV created with full history.")
