import os
import pandas as pd

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
dff_file_path = os.path.join(RAW_DATA_DIR, "interest_rate_decision_table.html")
output_path = os.path.join(PROCESSED_DATA_DIR, "federal_interest_rate.csv")

# -----------------------------------------------------------------------------
# Step 3: Read the HTML file (instead of using pd.read_csv)
#         read_html returns a list of DataFrames, one per <table> found in the HTML.
# -----------------------------------------------------------------------------
dfs = pd.read_html(dff_file_path)  # might raise ValueError if no table is found
dff_data = dfs[0]                  # Take the first table, or adjust index if multiple

# (Optional) Check columns
# print(dff_data.columns)

# -----------------------------------------------------------------------------
# Step 4: Rename columns if necessary
#         Suppose your table columns are something like:
#         [ "Date", "Rate" ]
#         We rename them to "observation_date" and "DFF" for consistency
# -----------------------------------------------------------------------------
dff_data = dff_data.rename(columns={
    dff_data.columns[0]: "observation_date",  # first column is date
    dff_data.columns[1]: "DFF"                # second column is the rate
})

# -----------------------------------------------------------------------------
# Step 5: Convert "observation_date" to datetime and split into Year/Month/Day
# -----------------------------------------------------------------------------
dff_data["observation_date"] = pd.to_datetime(dff_data["observation_date"], errors="coerce")
# Drop rows where date didn't parse
dff_data.dropna(subset=["observation_date"], inplace=True)

dff_data["Year"] = dff_data["observation_date"].dt.year
dff_data["Month"] = dff_data["observation_date"].dt.month
dff_data["Day"] = dff_data["observation_date"].dt.day

# -----------------------------------------------------------------------------
# Step 6: Rearrange columns
# -----------------------------------------------------------------------------
dff_data_transformed = dff_data[["Year", "Month", "Day", "DFF"]]

# -----------------------------------------------------------------------------
# Step 7: Save the transformed data to a CSV file
# -----------------------------------------------------------------------------
dff_data_transformed.to_csv(output_path, index=False)
print(f"DFF data has been transformed and saved to '{output_path}'")
