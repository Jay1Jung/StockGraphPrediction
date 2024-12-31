import yfinance as yf
import pandas as pd
import os


def get_stock_data(ticker, start_date, end_date, output_file):
    try:
        # Fetch the data from Yahoo Finance
        stock_data = yf.download(ticker, start=start_date, end=end_date)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Save to CSV
        stock_data.to_csv(output_file)
        print(f"Stock data for {ticker} has been saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    ticker = input("Enter the stock ticker (e.g., AAPL for Apple): ").strip()
    start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter the end date (YYYY-MM-DD): ").strip()
    output_file = input("Enter the output file path (e.g., './data/AAPL_stock_data.csv'): ").strip()

    get_stock_data(ticker, start_date, end_date, output_file)
