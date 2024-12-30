import os
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Step 1: Dynamically set PROJECT_ROOT
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
PLOT_DIR = os.path.join(PROJECT_ROOT, "plots")

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)

# Step 2: Fetch S&P 500 data from Yahoo Finance
sp500 = yf.Ticker("^GSPC")  # Yahoo Finance symbol for S&P 500
data = sp500.history(period="10y")  # Get 10 years of historical data

"""
# Preview the data
print("S&P 500 data preview:")
print(data.head())
"""

# Step 3: Save data to CSV in the processed data directory
csv_file = os.path.join(PROCESSED_DATA_DIR, "sp500_data.csv")
data.to_csv(csv_file)
print(f"S&P 500 data saved to {csv_file}")

# Step 4: Plot S&P 500 Closing Prices
plt.figure(figsize=(12, 6))
plt.plot(data.index, data["Close"], label="S&P 500 Close", color="r")
plt.xlabel("Date")
plt.ylabel("Closing Price (USD)")
plt.title("S&P 500 Closing Prices (Last 10 Years)")
plt.legend()
plt.tight_layout()

# Save the plot to the plots directory
plot_file = os.path.join(PLOT_DIR, "sp500_closing_prices.png")
plt.savefig(plot_file)
print(f"Plot saved as {plot_file}")
# plt.show()  # printing plot
