import os
import pandas as pd
import calendar

# Step 1: Dynamically set PROJECT_ROOT
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Step 2: File paths
cpi_file_path = os.path.join(RAW_DATA_DIR, "GDP.csv")
expanded_output_path = os.path.join(PROCESSED_DATA_DIR, "GDP_expanded.csv")

# Step 3: Load the GDP data
cpi_data = pd.read_csv(cpi_file_path)

# Reshape the GDP data to have Year and GDP columns
cpi_long_format = cpi_data.melt(
    id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
    var_name="Year",
    value_name="GDP"
)

# Step 4: Filter data for valid years and from 2000 onwards
cpi_long_format = cpi_long_format[cpi_long_format["Year"].str.isdigit()]
cpi_filtered = cpi_long_format[cpi_long_format["Year"].astype(int) >= 2000].copy()

# Step 5: Expand rows for each day of the year
expanded_rows = []

for _, row in cpi_filtered.iterrows():
    year = int(row["Year"])
    gdp_value = row["GDP"]
    for month in range(1, 13):  # Months from 1 (January) to 12 (December)
        days_in_month = calendar.monthrange(year, month)[1]
        for day in range(1, days_in_month + 1):
            expanded_rows.append({"Year": year, "Month": month, "Day": day, "GDP": gdp_value})

# Create a new DataFrame with the expanded data
cpi_expanded = pd.DataFrame(expanded_rows)

# Step 6: Save the expanded data to a CSV file
cpi_expanded.to_csv(expanded_output_path, index=False)

print(f"Expanded GDP data has been saved to {expanded_output_path}")
