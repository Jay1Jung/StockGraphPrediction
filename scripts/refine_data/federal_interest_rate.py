import os
import pandas as pd
import calendar
import sys

# ----------------------------- #
# **1. Setup Project Paths**
# ----------------------------- #

# Step 1: Dynamically set PROJECT_ROOT
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Step 2: Define file paths
interest_rate_file_path = os.path.join(RAW_DATA_DIR, "interest_rate_decision_table.html")
output_path = os.path.join(PROCESSED_DATA_DIR, "federal_interest_rate.csv")

# ----------------------------- #
# **2. Read HTML Tables**
# ----------------------------- #

# Step 3: Read the HTML file and extract all tables
try:
    dfs = pd.read_html(interest_rate_file_path)
    print(f"Number of tables found: {len(dfs)}")
except ValueError as e:
    sys.exit(f"[ERROR] Error reading HTML tables: {e}")

# Ensure at least one table is found
if len(dfs) == 0:
    sys.exit("[ERROR] No tables found in the HTML file.")

# Step 4: Inspect each table's columns to identify the correct one
print("\n--- Inspecting Tables ---")
for i, table in enumerate(dfs):
    print(f"\nTable {i} columns: {table.columns.tolist()}")

# Step 5: Select the Correct Table
# Define required columns based on sample data
required_columns = ["Release Date", "Time", "Actual", "Forecast", "Previous"]

def find_correct_table(tables, required_cols):
    """
    Finds the table that contains all required columns.
    
    Parameters:
        tables (list of pd.DataFrame): List of tables extracted from HTML.
        required_cols (list of str): List of required column names.
        
    Returns:
        pd.DataFrame: The table that contains all required columns.
        
    Raises:
        ValueError: If no table contains all required columns.
    """
    for idx, table in enumerate(tables):
        if all(col in table.columns for col in required_cols):
            print(f"\n[INFO] Found the correct table at index {idx}")
            return table
    raise ValueError("No table with the required columns found.")

# Select the table containing all required columns
try:
    dff_data = find_correct_table(dfs, required_columns)
except ValueError as e:
    sys.exit(f"[ERROR] {e}")

print("\nSelected Table Columns:", dff_data.columns.tolist())

# ----------------------------- #
# **3. Rename Columns Appropriately**
# ----------------------------- #

# Step 6: Rename Columns Based on Column Names
# This ensures that even if column names have slight variations, they are standardized

# Initialize an empty dictionary for column mapping
column_mapping = {}

for col in dff_data.columns:
    col_lower = col.lower()
    if "release date" in col_lower or "date" in col_lower:
        column_mapping[col] = "observation_date"
    elif "actual" in col_lower:
        column_mapping[col] = "Actual"
    elif "forecast" in col_lower:
        column_mapping[col] = "Forecast"
    elif "previous" in col_lower:
        column_mapping[col] = "Previous"
    elif "time" in col_lower:
        column_mapping[col] = "Time"
    else:
        # If there are other columns, decide whether to keep or rename them
        column_mapping[col] = col  # Keep the original name

print("\nColumn Mapping:", column_mapping)

# Apply the column renaming
dff_data = dff_data.rename(columns=column_mapping)

print("\nRenamed Columns:", dff_data.columns.tolist())

# ----------------------------- #
# **4. Verify Required Columns Exist**
# ----------------------------- #

# Step 7: Ensure all required columns are present after renaming
required_columns_standard = ["observation_date", "Time", "Actual", "Forecast", "Previous"]

for col in required_columns_standard:
    if col not in dff_data.columns:
        sys.exit(f"[ERROR] Required column '{col}' not found in the data.")

print("\n[INFO] All required columns are present.")

# ----------------------------- #
# **5. Parse and Clean Data**
# ----------------------------- #

# Step 8: Convert "observation_date" to datetime and handle parsing
def extract_date(date_str):
    """
    Extracts the date part from a string like "Dec 19, 2024 (Nov)".
    Returns a datetime object.
    """
    try:
        # Split the string at the first parenthesis and take the first part
        date_part = date_str.split('(')[0].strip()
        # Parse the date
        return pd.to_datetime(date_part, format="%b %d, %Y")
    except Exception as e:
        print(f"[WARNING] Error parsing date '{date_str}': {e}")
        return pd.NaT

# Apply the date extraction function
dff_data["observation_date"] = dff_data["observation_date"].apply(extract_date)

# Drop rows where date parsing failed
initial_row_count = len(dff_data)
dff_data.dropna(subset=["observation_date"], inplace=True)
dropped_rows = initial_row_count - len(dff_data)
if dropped_rows > 0:
    print(f"[WARNING] Dropped {dropped_rows} rows due to invalid dates.")

# Step 9: Split "observation_date" into Year, Month, Day
dff_data["Year"] = dff_data["observation_date"].dt.year
dff_data["Month"] = dff_data["observation_date"].dt.month
dff_data["Day"] = dff_data["observation_date"].dt.day

print("\n[INFO] Date parsing and splitting completed.")

# Step 10: Clean the "Actual", "Forecast", and "Previous" Columns
def clean_rate_column(rate_series, column_name):
    """
    Cleans rate columns by removing percentage signs and converting to float.
    
    Parameters:
        rate_series (pd.Series): The rate column to clean.
        column_name (str): The name of the column (for logging).
        
    Returns:
        pd.Series: Cleaned and numeric rate values.
    """
    cleaned = rate_series.astype(str).str.replace('%', '').str.replace(',', '').str.strip()
    cleaned = pd.to_numeric(cleaned, errors='coerce')
    return cleaned

# Clean "Actual" column
dff_data["Actual"] = clean_rate_column(dff_data["Actual"], "Actual")

# Clean "Forecast" column
dff_data["Forecast"] = clean_rate_column(dff_data["Forecast"], "Forecast")

# Clean "Previous" column
dff_data["Previous"] = clean_rate_column(dff_data["Previous"], "Previous")

# Drop rows with invalid "Actual", "Forecast", or "Previous" values
for col in ["Actual", "Forecast", "Previous"]:
    initial_row_count = len(dff_data)
    dff_data.dropna(subset=[col], inplace=True)
    dropped_rows = initial_row_count - len(dff_data)
    if dropped_rows > 0:
        print(f"[WARNING] Dropped {dropped_rows} rows due to invalid {col} values.")

print("\n[INFO] 'Actual', 'Forecast', and 'Previous' columns cleaned and converted to numeric.")

# ----------------------------- #
# **6. Expand Data to Daily Records (Optional)**
# ----------------------------- #

# Step 11: Expand rows for each day between observations
# This assigns the latest available interest rates to each day until the next observation

# Sort the data by date
dff_data.sort_values("observation_date", inplace=True)

# Reset index
dff_data.reset_index(drop=True, inplace=True)

# Initialize list for expanded rows
expanded_rows = []

print("\n[INFO] Expanding rows to daily records...")

for idx, row in dff_data.iterrows():
    current_date = row["observation_date"]
    if idx < len(dff_data) - 1:
        next_date = dff_data.loc[idx + 1, "observation_date"]
    else:
        # For the last observation, set the next_date to end of year
        next_date = pd.Timestamp(year=current_date.year, month=12, day=31)
    
    # Generate date range from current_date to day before next_date
    date_range = pd.date_range(start=current_date, end=next_date - pd.Timedelta(days=1), freq='D')
    
    for single_date in date_range:
        expanded_rows.append({
            "Year": single_date.year,
            "Month": single_date.month,
            "Day": single_date.day,
            "Time": row["Time"],
            "Actual": row["Actual"],
            "Forecast": row["Forecast"],
            "Previous": row["Previous"]
        })

# Step 12: Create expanded DataFrame
expanded_data = pd.DataFrame(expanded_rows)

print(f"\n[INFO] Expanded data to {len(expanded_data)} daily records.")

# ----------------------------- #
# **7. Save and Validate the Transformed Data**
# ----------------------------- #

# Step 13: Save the expanded data to CSV
expanded_data.to_csv(output_path, index=False)
print(f"\n[INFO] Expanded interest rate data has been saved to '{output_path}'")

# Step 14: Validate Saved CSV
try:
    saved_data = pd.read_csv(output_path)
    print("\n--- Validating Saved CSV ---")
    print(saved_data.head())
    print(f"Total rows saved: {len(saved_data)}")
except Exception as e:
    print(f"[ERROR] Error reading the saved CSV: {e}")
