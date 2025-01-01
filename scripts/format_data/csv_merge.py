import os
import pandas as pd

# Step 1: Set up project directory paths dynamically
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "formatted")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "formatted")

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Step 2: File paths for all uploaded files
file_paths = [
    os.path.join(RAW_DATA_DIR, "formatted_cpi_data.csv"),
    os.path.join(RAW_DATA_DIR, "formatted_UnemploymentRate.csv"),
    os.path.join(RAW_DATA_DIR, "formatted_us_leading_index.csv"),
    os.path.join(RAW_DATA_DIR, "formatted_us_nominal_GDP.csv"),
    os.path.join(RAW_DATA_DIR, "merged_pmi_data.csv"),
    os.path.join(RAW_DATA_DIR, "merged_stock_data.csv"),
    os.path.join(RAW_DATA_DIR, "processed_sp500_data.csv")
]

# Step 3: Load and merge all CSV files
final_data = None

for file_path in file_paths:
    temp_data = pd.read_csv(file_path)
    temp_data['Date'] = pd.to_datetime(temp_data['Date'], errors='coerce')
    if final_data is None:
        final_data = temp_data
    else:
        final_data = pd.merge(final_data, temp_data, on='Date', how='outer')

# Step 4: Rename columns for clarity
final_data = final_data.rename(columns={
    'Actual_x': 'CPI',
    'Actual_y': 'Unemployment Rate',
    'LeadingIndex' : 'Leading_index',
    'Closing price' : 's&p 500 closing_price'
})

# Step 5: Sort the merged data by Date
final_data = final_data.sort_values(by='Date')

# Step 6: Save the merged data to a CSV file
output_file_path = os.path.join(PROCESSED_DATA_DIR, "merged_all_data.csv")
final_data.to_csv(output_file_path, index=False)

print(f"All data merged and saved as {output_file_path}")
