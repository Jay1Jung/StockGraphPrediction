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

def process_unemployment_rate_data(input_dir, output_dir):
    for file_name in os.listdir(input_dir):
        # Process only the file named "unemployment_rate.csv"
        if "unemployment" in file_name.lower() and file_name.endswith(".csv"):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_path = os.path.join(output_dir, "formatted_" + file_name)

            try:
                # Load the CSV file
                data = pd.read_csv(input_file_path)

                # Keep only the Release Date and Actual columns
                filtered_data = data[["Release Date", "Actual"]]

                # Convert "Release Date" to the format YYYY-MM-DD
                filtered_data["Release Date"] = pd.to_datetime(
                    filtered_data["Release Date"].str.split('(').str[0].str.strip(),
                    format="%b %d, %Y"
                ).dt.strftime("%Y-%m-%d")

                # Filter for dates from 2020 and later
                filtered_data["Release Date"] = pd.to_datetime(filtered_data["Release Date"])
                filtered_data = filtered_data[filtered_data["Release Date"].dt.year >= 2020]

                # Convert "Actual" from percentage to decimal
                filtered_data["Actual"] = filtered_data["Actual"].str.rstrip('%').astype(float) / 100

                # Rename columns for consistency
                filtered_data.rename(columns={"Release Date": "Date"}, inplace=True)

                # Save the processed data to a new file
                filtered_data.to_csv(output_file_path, index=False)

                print(f"Processed unemployment rate data saved to: {output_file_path}")
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

# Run the function
process_unemployment_rate_data(RAW_DATA_DIR, PROCESSED_DATA_DIR)
