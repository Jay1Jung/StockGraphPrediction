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

def process_gdp_files_with_date_filter(input_dir, output_dir):
    for file_name in os.listdir(input_dir):
        # Process only files containing "gdp" in the name
        if "gdp" in file_name.lower() and file_name.endswith(".csv"):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_path = os.path.join(output_dir, "formatted_" + file_name)

            try:
                # Load the CSV file
                data = pd.read_csv(input_file_path)

                # Combine Year, Month, and Day into a single Date column
                data["Date"] = pd.to_datetime(
                    data["Year"].astype(str) + " " + data["Month"].astype(str) + " " + data["Day"].astype(str),
                    format="%Y %m %d"
                ).dt.strftime("%Y-%m-%d")  # Convert to YYYY-MM-DD format

                # Keep only the Date and Actual columns
                filtered_data = data[["Date", "GDP"]]

                # Filter data for dates after 2020
                filtered_data["Date"] = pd.to_datetime(filtered_data["Date"])
                filtered_data = filtered_data[filtered_data["Date"].dt.year >= 2020]

                # Save the processed data to a new file
                filtered_data.to_csv(output_file_path, index=False)

                print(f"Processed GDP data saved to: {output_file_path}")
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

# Run the function
process_gdp_files_with_date_filter(RAW_DATA_DIR, PROCESSED_DATA_DIR)
