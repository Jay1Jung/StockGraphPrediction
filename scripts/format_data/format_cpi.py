import os
import pandas as pd

# Set up dynamic paths
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")  # Input path
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "formatted")  # Output path

# Ensure the output directory exists
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def process_cpi_data_with_year_month_day(input_file_name, output_file_name):
    # Construct input and output file paths
    input_file_path = os.path.join(RAW_DATA_DIR, input_file_name)
    output_file_path = os.path.join(PROCESSED_DATA_DIR, output_file_name)

    try:
        # Load the CSV file
        data = pd.read_csv(input_file_path)

        # Combine Year, Month, and Day into a single Date column
        data["Date"] = pd.to_datetime(
            data["Year"].astype(str) + " " + data["Month"] + " " + data["Day"].astype(str),
            format="%Y %b %d"
        ).dt.strftime("%Y-%m-%d")  # Convert to YYYY-MM-DD format

        # Convert "Actual" from percentage to decimal
        data["Actual"] = data["Actual"].str.rstrip('%').astype(float) / 100

        # Keep only the Date and Actual columns
        filtered_data = data[["Date", "Actual"]]

        # Filter data for dates after 2020
        filtered_data["Date"] = pd.to_datetime(filtered_data["Date"])
        filtered_data = filtered_data[filtered_data["Date"].dt.year >= 2020]

        # Save the processed data to a new file
        filtered_data.to_csv(output_file_path, index=False)

        print(f"Processed CPI data saved to: {output_file_path}")
    except Exception as e:
        print(f"Error processing CPI file: {e}")

# Example: Process the CPI file
process_cpi_data_with_year_month_day("us_cpi.csv", "formatted_cpi_data.csv")
