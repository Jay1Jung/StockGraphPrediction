import os
import pandas as pd
import calendar
import sys

# Step 1: Dynamically set PROJECT_ROOT
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Step 2: File paths
gdp_file_path = os.path.join(RAW_DATA_DIR, "us_nominal_gdp.csv")
expanded_output_path = os.path.join(PROCESSED_DATA_DIR, "us_nominal_GDP.csv")

# print(f"[DEBUG] Reading CSV from: {gdp_file_path}")
if not os.path.exists(gdp_file_path):
    sys.exit(f"[ERROR] File not found: {gdp_file_path}")

# Step 3: Load the GDP data
gdp_data = pd.read_csv(gdp_file_path)
# print("[DEBUG] Columns in gdp_data:", gdp_data.columns.tolist())
# print("[DEBUG] Data types in gdp_data (before conversion):\n", gdp_data.dtypes)

# Step 4: Ensure the 'Year' column is numeric and integer
#         1) Convert to numeric
#         2) Drop rows with NaN in 'Year'
#         3) Cast to int
gdp_data["Year"] = pd.to_numeric(gdp_data["Year"], errors="coerce")
rows_before = len(gdp_data)
gdp_data.dropna(subset=["Year"], inplace=True)
rows_after = len(gdp_data)
# print(f"[DEBUG] Dropped {rows_before - rows_after} rows where 'Year' was invalid/NaN.")
 
gdp_data["Year"] = gdp_data["Year"].astype(int)
# print("[DEBUG] Data types in gdp_data (after conversion to int):\n", gdp_data.dtypes)

# Optional: filter for Year >= 2000
gdp_data = gdp_data[gdp_data["Year"] >= 2000].copy()
# print("[DEBUG] Rows remaining after filtering Year >= 2000:", len(gdp_data))

# Step 5: Expand rows for each day of each year
expanded_rows = []

# print("\n[DEBUG] Expanding rows now...")
for idx, row in gdp_data.iterrows():
    # Even though we cast to int, let's forcibly cast again in the loop for safety:
    year_float = row["Year"]  # might be float if something re-converted it
    year = int(year_float)

    # Print row index and types
    # print(f"  Row idx={idx}, raw year={row['Year']} -> final year={year}, type(year)={type(year)}")

    gdp_value = row.get("Nominal GDP (Current US$)", None)
    if gdp_value is None:
        # If there's no such column, print a warning and skip
        print(f"[WARNING] Row idx={idx} has no 'Nominal GDP (Current US$)' column. Row data: {row}")
        continue

    # Now do the month/day expansion
    for month in range(1, 13):
        try:
            days_in_month = calendar.monthrange(year, month)[1]
        except Exception as e:
            # Print a debug message if it fails
            print(f"[ERROR] monthrange({year}, {month}) failed on row index={idx} with error: {e}")
            print("[DEBUG] Full row data:\n", row)
            raise  # re-raise the error so we can see the traceback
        for day in range(1, days_in_month + 1):
            expanded_rows.append({
                "Year": year,
                "Month": month,
                "Day": day,
                "GDP": gdp_value
            })

# Step 6: Save expanded data
gdp_expanded = pd.DataFrame(expanded_rows)
gdp_expanded.to_csv(expanded_output_path, index=False)
print("Expanded GDP data has been saved to {expanded_output_path}")
