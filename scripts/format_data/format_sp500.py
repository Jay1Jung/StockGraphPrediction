import os
import pandas as pd

# Step 1: Set up project directory paths dynamically
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "formatted")

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Step 2: File paths
input_file_path = os.path.join(RAW_DATA_DIR, "sp500_data.csv")
output_file_path = os.path.join(PROCESSED_DATA_DIR, "processed_sp500_data.csv")

# Step 3: Load the CSV file
data = pd.read_csv(input_file_path)

# Step 4: Process the 'Date' column
data['Date'] = pd.to_datetime(
    data['Date'].astype(str).str.replace(r'-\d{2}:\d{2}$', '', regex=True),
    errors='coerce'
)

# Step 5: Extract Year, Month, and Day
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month
data['Day'] = data['Date'].dt.day

# Step 6: Rename 'Close' column to 'Closing price'
data = data.rename(columns={'Close': 'Closing price'})

# Step 7: Select necessary columns
processed_data = data[['Year', 'Month', 'Day', 'Closing price']]

# Step 8: Save the processed data to a CSV file
processed_data.to_csv(output_file_path, index=False)

print(f"Data processed and saved as {output_file_path}")
