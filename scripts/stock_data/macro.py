import os
import pandas as pd
import yfinance as yf

# ------------------------------------------------------------------------
# 1) The incremental download function (enhanced to handle both earlier and newer data)
# ------------------------------------------------------------------------
def incremental_download(ticker, output_dir, start_date, end_date):
    """
    Incrementally download data for a single ticker from yfinance.
    If a CSV for this ticker already exists, fetch new data from the last date
    and/or earlier data if start_date has been moved back.
    """
    csv_path = os.path.join(output_dir, f"{ticker}.csv")

    if os.path.exists(csv_path):
        # Load existing data
        existing_df = pd.read_csv(csv_path)

        # Ensure 'Date' is datetime
        if "Date" in existing_df.columns:
            existing_df["Date"] = pd.to_datetime(existing_df["Date"])
        else:
            raise ValueError(f"Existing CSV for {ticker} has unexpected format (no 'Date' column).")

        min_existing_date = existing_df["Date"].min()
        max_existing_date = existing_df["Date"].max()

        # Initialize list to hold new data chunks
        new_data = []

        # Check if we need to download earlier data
        if pd.to_datetime(start_date) < min_existing_date:
            download_start_earlier = start_date
            download_end_earlier = (min_existing_date - pd.Timedelta(days=1)).strftime('%Y-%m-%d')
            print(f"{ticker}: Downloading earlier data from {download_start_earlier} to {download_end_earlier}...")
            df_earlier = yf.download(ticker, start=download_start_earlier, end=download_end_earlier)
            if not df_earlier.empty:
                df_earlier.reset_index(inplace=True)
                df_earlier["Date"] = pd.to_datetime(df_earlier["Date"])
                new_data.append(df_earlier)
            else:
                print(f"{ticker}: No earlier data returned by yfinance.")

        # Check if we need to download newer data
        if pd.to_datetime(end_date) > max_existing_date:
            download_start_newer = (max_existing_date + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
            download_end_newer = end_date
            print(f"{ticker}: Downloading newer data from {download_start_newer} to {download_end_newer}...")
            df_newer = yf.download(ticker, start=download_start_newer, end=download_end_newer)
            if not df_newer.empty:
                df_newer.reset_index(inplace=True)
                df_newer["Date"] = pd.to_datetime(df_newer["Date"])
                new_data.append(df_newer)
            else:
                print(f"{ticker}: No newer data returned by yfinance.")

        # If there's new data, merge it with existing data
        if new_data:
            combined_df = existing_df.copy()

            for df in new_data:
                if df["Date"].min() < combined_df["Date"].min():
                    # Prepend earlier data
                    combined_df = pd.concat([df, combined_df], ignore_index=True)
                else:
                    # Append newer data
                    combined_df = pd.concat([combined_df, df], ignore_index=True)

            # Remove duplicate dates
            combined_df.drop_duplicates(subset=["Date"], keep="last", inplace=True)

            # Sort by Date
            combined_df.sort_values("Date", inplace=True)

            # Save updated data
            combined_df.to_csv(csv_path, index=False)
            total_new_rows = sum(len(df) for df in new_data)
            print(f"{ticker}: CSV updated with {total_new_rows} new rows.")
        else:
            print(f"{ticker}: No new data to download.")

    else:
        # No existing CSV -> fetch full data
        print(f"{ticker}: No existing CSV found. Downloading full history from {start_date} to {end_date}...")
        df = yf.download(ticker, start=start_date, end=end_date)
        if df.empty:
            print(f"{ticker}: No data returned by yfinance.")
            return

        df.reset_index(inplace=True)
        df["Date"] = pd.to_datetime(df["Date"])
        df.to_csv(csv_path, index=False)
        print(f"{ticker}: CSV created with full history.")

# ------------------------------------------------------------------------
# 2) Top-level code that reads tickers.txt and downloads them
# ------------------------------------------------------------------------

# Dynamically find the project root, assuming this script is in:
# StockGraphPrediction/scripts/ or somewhere under the repo
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))  # adjust ".." as needed

# Path to tickers.txt in StockGraphPrediction/data/stock_data/
ticker_file = os.path.join(PROJECT_ROOT, "tickers.txt")

# Path to data/stock_data for output
output_dir = os.path.join(PROJECT_ROOT, "data", "stock_data")
os.makedirs(output_dir, exist_ok=True)

# Read all tickers from tickers.txt
with open(ticker_file, "r", encoding="utf-8") as f:
    lines = f.readlines()
tickers = [line.strip() for line in lines if line.strip()]

# Define date range
start_date = "2020-01-01"
end_date   = "2024-12-15"

# Download incrementally for each ticker
for tkr in tickers:
    incremental_download(tkr, output_dir, start_date, end_date)
