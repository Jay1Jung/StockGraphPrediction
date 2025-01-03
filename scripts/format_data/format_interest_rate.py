import os
import pandas as pd
import sys
# Step 1: Dynamically set PROJECT_ROOT
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")    # Assuming 'federal_interest_rate.csv' is here
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "formatted")

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Step 2: Define the input and output file paths
input_file_path = os.path.join(RAW_DATA_DIR, "federal_interest_rate.csv")
output_file_path = os.path.join(PROCESSED_DATA_DIR, "formatted_interest_rate_data.csv")

# Check if the input file exists
if not os.path.exists(input_file_path):
    sys.exit(f"[ERROR] Input file not found at: {input_file_path}")
else:
    print(f"Found input file at: {input_file_path}")

# Step 3: Load the CSV file
try:
    df = pd.read_csv(input_file_path)
except Exception as e:
    sys.exit(f"[ERROR] Failed to read CSV file: {e}")

# Inspect the columns (optional)
# Step 4: Ensure required columns are present
required_columns = ['Year', 'Month', 'Day', 'Time', 'Actual', 'Forecast', 'Previous']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    sys.exit(f"[ERROR] Missing expected columns: {missing_columns}")

# Step 5: Combine 'Year', 'Month', 'Day' into 'Date' in 'yyyy-mm-dd' format
try:
    # Ensure 'Year', 'Month', 'Day' are numeric
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype('Int64')
    df['Month'] = pd.to_numeric(df['Month'], errors='coerce').astype('Int64')
    df['Day'] = pd.to_numeric(df['Day'], errors='coerce').astype('Int64')
    
    # Drop rows with NaN in 'Year', 'Month', or 'Day'
    initial_row_count = len(df)
    df.dropna(subset=['Year', 'Month', 'Day'], inplace=True)
    dropped_rows = initial_row_count - len(df)
    if dropped_rows > 0:
        print(f"[WARNING] Dropped {dropped_rows} rows due to invalid 'Year', 'Month', or 'Day' values.")
    
    # Create 'Date' column
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']], errors='coerce')
    
    # Drop rows where 'Date' couldn't be created
    initial_row_count = len(df)
    df.dropna(subset=['Date'], inplace=True)
    dropped_rows = initial_row_count - len(df)
    if dropped_rows > 0:
        print(f"[WARNING] Dropped {dropped_rows} rows due to invalid 'Date' values.")
    
    # Format 'Date' to 'yyyy-mm-dd'
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
except Exception as e:
    sys.exit(f"[ERROR] Failed to create 'Date' column: {e}")

# Step 6: Ensure 'Time' is in 'HH:MM' format
try:
    # Convert 'Time' to string and strip whitespace
    df['Time'] = df['Time'].astype(str).str.strip()
    
    # Convert to datetime to validate format and reformat to 'HH:MM'
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M', errors='coerce').dt.strftime('%H:%M')
    
    # Drop rows with invalid 'Time' formats
    initial_row_count = len(df)
    df.dropna(subset=['Time'], inplace=True)
    dropped_rows = initial_row_count - len(df)
    if dropped_rows > 0:
        print(f"[WARNING] Dropped {dropped_rows} rows due to invalid 'Time' format.")
    
except Exception as e:
    sys.exit(f"[ERROR] Failed to clean 'Time' column: {e}")

# Step 7: Convert 'Actual', 'Forecast', 'Previous' from percentage strings to float decimals
def convert_percentage_to_decimal(series, column_name):
    try:
        # Remove any percentage signs, commas, and whitespace
        series_cleaned = series.astype(str).str.replace('%', '').str.replace(',', '').str.strip()
        # Convert to float and divide by 100 to get decimal
        decimal_series = series_cleaned.astype(float) / 100
        return decimal_series
    except Exception as e:
        sys.exit(f"[ERROR] Failed to convert '{column_name}' from percentage to decimal: {e}")

# Apply conversion
df['Interest_rate'] = convert_percentage_to_decimal(df['Actual'], 'Actual')
df['Forecast'] = convert_percentage_to_decimal(df['Forecast'], 'Forecast')
df['Previous'] = convert_percentage_to_decimal(df['Previous'], 'Previous')

# Drop the original 'Actual' column as it's now converted to 'Interest_rate'
df.drop(columns=['Actual'], inplace=True)

# Drop rows with NaN in 'Interest_rate', 'Forecast', or 'Previous'
initial_row_count = len(df)
df.dropna(subset=['Interest_rate', 'Forecast', 'Previous'], inplace=True)
dropped_rows = initial_row_count - len(df)
if dropped_rows > 0:
    print(f"[WARNING] Dropped {dropped_rows} rows due to invalid 'Interest_rate', 'Forecast', or 'Previous' values.")


# Step 8: Select only the desired columns for output
desired_columns = ['Date', 'Time', 'Interest_rate', 'Forecast', 'Previous']
df = df[desired_columns]

# Step 9: Filter data for dates on or after 2020-01-01
try:
    # Convert 'Date' to datetime for filtering
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
    
    # Drop rows where 'Date' couldn't be parsed
    initial_row_count = len(df)
    df.dropna(subset=['Date'], inplace=True)
    dropped_rows = initial_row_count - len(df)
    if dropped_rows > 0:
        print(f"[WARNING] Dropped {dropped_rows} rows due to invalid 'Date' formats during filtering.")
    
    # Apply the date filter
    df = df[df['Date'] >= pd.Timestamp('2020-01-01')]
    
    # Convert 'Date' back to string in 'yyyy-mm-dd' format
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
except Exception as e:
    sys.exit(f"[ERROR] Failed to filter data based on 'Date': {e}")

# Step 10: Save the processed data to a CSV file
try:
    df.to_csv(output_file_path, index=False)
    print(f"Processed data saved to: {output_file_path}")
except Exception as e:
    sys.exit(f"[ERROR] Failed to save processed data: {e}")
