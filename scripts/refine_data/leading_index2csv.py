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
unemployment_rate_file_path = os.path.join(RAW_DATA_DIR, "Unemploymentrate.csv")
expanded_output_path = os.path.join(PROCESSED_DATA_DIR, "UnemploymentRate_expanded.csv")

# Step 3: Load the Unemployment Rate data
unemployment_rate_data = pd.read_csv(unemployment_rate_file_path)

# Step 4: Reshape the data to have Year and OBS_VALUE columns
unemployment_rate_data_long = unemployment_rate_data.melt(
    id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
    var_name="Year",
    value_name="OBS_VALUE"
)

# Step 5: Filter out rows where the Year column is not numeric and for years >= 2000
unemployment_rate_data_long = unemployment_rate_data_long[unemployment_rate_data_long["Year"].str.isdigit()]
unemployment_rate_data_long["Year"] = unemployment_rate_data_long["Year"].astype(int)
unemployment_rate_data_long = unemployment_rate_data_long[unemployment_rate_data_long["Year"] >= 2000]

# Step 6: Generate all dates for each month and assign the OBS_VALUE to each day
expanded_rows = []

for _, row in unemployment_rate_data_long.iterrows():
    year = row["Year"]
    obs_value = row["OBS_VALUE"]
    for month in range(1, 13):  # From January (1) to December (12)
        days_in_month = calendar.monthrange(year, month)[1]
        for day in range(1, days_in_month + 1):
            expanded_rows.append({"Year": year, "Month": month, "Day": day, "Unemployment_rate": obs_value})

# Step 7: Create a new DataFrame with the expanded data
unemployment_rate_expanded = pd.DataFrame(expanded_rows)

# Step 8: Save the expanded data to a CSV file
unemployment_rate_expanded.to_csv(expanded_output_path, index=False)

print(f"Expanded Unemployment Rate data has been saved to {expanded_output_path}")
