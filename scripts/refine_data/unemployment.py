import os
import pandas as pd

# Step 1: Set up paths dynamically
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))  # Two levels up from this file
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Input and output file paths
html_file_path = os.path.join(RAW_DATA_DIR, "unemployment_rate_table.html")  # HTML source file
csv_output_path = os.path.join(PROCESSED_DATA_DIR, "unemploymentrate.csv")  # Processed CSV file

# Step 2: Load the HTML file into a DataFrame
try:
    # Assuming the table is the first one on the page
    unemployment_rate_data = pd.read_html(html_file_path)[0]
    print("Data successfully loaded from HTML file.")
except ValueError as e:
    raise ValueError(f"Error reading HTML file: {e}")

# Step 3: Display the first few rows and column names (for verification)
print("Loaded Data Preview:")
print(unemployment_rate_data.head())  # Preview the first 5 rows
print("Available Columns:", unemployment_rate_data.columns)  # List all columns

# Step 4: Save the DataFrame to a CSV file
unemployment_rate_data.to_csv(csv_output_path, index=False)
print(f"Data saved to CSV: {csv_output_path}")
