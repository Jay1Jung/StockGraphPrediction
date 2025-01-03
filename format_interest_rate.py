import os
import pandas as pd

# Define project root and data directories
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "formatted")

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Define the input and output file paths
input_file_path = os.path.join(RAW_DATA_DIR, "interest_rate_decision_table.html")
output_file_path = os.path.join(PROCESSED_DATA_DIR, "formatted_interest_rate_data.csv")

# Check if the input file exists
if not os.path.exists(input_file_path):
    print(f"Input file not found at: {input_file_path}")
else:
    # Load the HTML file and extract the table
    tables = pd.read_html(input_file_path)

    # Select the table and clean data
    df = tables[0]
    df.columns = ['Release Date', 'Time', 'Actual', 'Forecast', 'Previous', 'Extra']
    df = df[['Release Date', 'Actual']]

    # Convert 'Release Date' to ISO format (yyyy-mm-dd)
    df['Release Date'] = pd.to_datetime(df['Release Date'], format='%b %d, %Y').dt.strftime('%Y-%m-%d')

    # Convert 'Actual' from percentage to decimal
    df['Actual'] = df['Actual'].str.replace('%', '').astype(float) / 100

    # Rename columns
    df.rename(columns={'Release Date': 'Date', 'Actual': 'Interest_rate'}, inplace=True)

    # Filter data for dates after 2020
    df = df[pd.to_datetime(df['Date']) >= pd.Timestamp('2020-01-01')]

    # Save the processed data to a CSV file
    df.to_csv(output_file_path, index=False)

    print(f"Processed data saved to: {output_file_path}")
