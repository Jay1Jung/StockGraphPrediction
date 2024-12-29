import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Fetch S&P 500 data from Yahoo Finance
sp500 = yf.Ticker("^GSPC")  # Yahoo Finance symbol for S&P 500
data = sp500.history(period="10y")  # Get 10 years of historical data

# Preview the data
print(data.head())

# Save to CSV for later use
csv_file = "sp500_data.csv"
data.to_csv(csv_file)
print(f"S&P 500 data saved to {csv_file}")

# Plot S&P 500 Closing Prices
plt.figure(figsize=(12, 6))
plt.plot(data.index, data["Close"], label="S&P 500 Close", color="r")
plt.xlabel("Date")
plt.ylabel("Closing Price (USD)")
plt.title("S&P 500 Closing Prices (Last 10 Years)")
plt.legend()
plt.tight_layout()

# Save and show the plot
plot_file = "sp500_closing_prices.png"
plt.savefig(plot_file)
print(f"Plot saved as {plot_file}")
plt.show()
