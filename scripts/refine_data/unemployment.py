import os
import pandas as pd
import calendar

# Step 1: Set up paths dynamically
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Input and output file paths
unemployment_rate_file_path = os.path.join(RAW_DATA_DIR, "Unemploymentrate.csv")
expanded_output_path = os.path.join(PROCESSED_DATA_DIR, "UnemploymentRate.csv")

# Step 2: Load the data
unemployment_rate_data = pd.read_csv(unemployment_rate_file_path)

"""
# Step 3: Reshape the data (melt years into rows)
print("Original columns:", unemployment_rate_data.columns)
"""

# Melt the year columns into a long format
melted_data = unemployment_rate_data.melt(
    id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
    var_name="Year",
    value_name="OBS_VALUE"
)

# Convert "Year" to integers and drop rows without valid OBS_VALUE
melted_data["Year"] = pd.to_numeric(melted_data["Year"], errors="coerce")
melted_data = melted_data.dropna(subset=["OBS_VALUE"]).reset_index(drop=True)

# Filter for years >= 2000
filtered_data = melted_data[melted_data["Year"] >= 2000]

# Step 4: Expand rows to include each day of the month
expanded_rows = []
for _, row in filtered_data.iterrows():
    year = int(row["Year"])
    obs_value = row["OBS_VALUE"]
    # Assume data applies to all months in the year
    for month in range(1, 13):  # Months from January (1) to December (12)
        days_in_month = calendar.monthrange(year, month)[1]
        for day in range(1, days_in_month + 1):
            expanded_rows.append({"Year": year, "Month": month, "Day": day, "OBS_VALUE": obs_value})

# Create a new DataFrame with expanded rows
unemployment_rate_expanded = pd.DataFrame(expanded_rows)

# Step 5: Save the expanded data to a CSV file
unemployment_rate_expanded.to_csv(expanded_output_path, index=False)

print(f"Expanded Unemployment Rate data saved to {expanded_output_path}")
