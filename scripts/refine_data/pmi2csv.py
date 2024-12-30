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
services_pmi_file_path = os.path.join(RAW_DATA_DIR, "manufacturing_pmi.csv")
output_path = os.path.join(PROCESSED_DATA_DIR, "manufacturing_pmi_transformed.csv")

# Step 3: Load the services PMI data
services_pmi_data = pd.read_csv(services_pmi_file_path)

# Step 4: Convert the Date column to datetime format
services_pmi_data['Date'] = pd.to_datetime(services_pmi_data['Date'])

# Step 5: Extract Year, Month, and Day from the Date column
services_pmi_data['Year'] = services_pmi_data['Date'].dt.year
services_pmi_data['Month'] = services_pmi_data['Date'].dt.month
services_pmi_data['Day'] = services_pmi_data['Date'].dt.day

# Step 6: Rearrange columns to have Year, Month, Day, and Actual PMI values
services_pmi_transformed = services_pmi_data[['Year', 'Month', 'Day', 'Actual']]

# Step 7: Save the transformed data to a CSV file
services_pmi_transformed.to_csv(output_path, index=False)

print(f"Services PMI data has been transformed and saved to {output_path}")
