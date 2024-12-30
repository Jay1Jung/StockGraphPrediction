import os
import pandas as pd

# Step 1: Dynamically set PROJECT_ROOT
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Step 2: File paths
dff_file_path = os.path.join(RAW_DATA_DIR, "DFF.csv")
output_path = os.path.join(PROCESSED_DATA_DIR, "DFF_transformed.csv")

# Step 3: Load the DFF data
dff_data = pd.read_csv(dff_file_path)

# Step 4: Split the observation_date into Year, Month, and Day
dff_data['Year'] = pd.to_datetime(dff_data['observation_date']).dt.year
dff_data['Month'] = pd.to_datetime(dff_data['observation_date']).dt.month
dff_data['Day'] = pd.to_datetime(dff_data['observation_date']).dt.day

# Step 5: Rearrange columns to have Year, Month, Day, and DFF
dff_data_transformed = dff_data[['Year', 'Month', 'Day', 'DFF']]

# Step 6: Save the transformed data to a CSV file
dff_data_transformed.to_csv(output_path, index=False)

print(f"DFF data has been transformed and saved to {output_path}")
