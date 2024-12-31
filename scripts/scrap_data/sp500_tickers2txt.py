import os
import pandas as pd

# 1) URL for S&P 500 listing on Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# 2) Read all HTML tables on the page
tables = pd.read_html(url)

print(f"Found {len(tables)} tables on the page.")

# 3) Inspect each table’s columns and shape
sp500_df = None
for i, df in enumerate(tables):
    print(f"\n--- TABLE {i} ---")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Shape: {df.shape}")
    # If it has a 'Symbol' column, assume it's the S&P 500 data
    if "Symbol" in df.columns:
        sp500_df = df
        print(">> This table has 'Symbol' column. We'll use this one.")
        break

if sp500_df is None:
    raise ValueError("Could not find a table with 'Symbol' column on this page.")

# 4) Extract the 'Symbol' column
tickers = sp500_df["Symbol"].tolist()
print(f"\nExtracted {len(tickers)} tickers.")

# 5) Write them to tickers.txt
output_file = "tickers.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for ticker in tickers:
        f.write(f"{ticker}\n")

print(f"Successfully wrote tickers to '{output_file}'.")
