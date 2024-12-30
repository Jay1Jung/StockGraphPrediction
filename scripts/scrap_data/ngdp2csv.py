import requests
import os
import pandas as pd

# Step 1: Define the API URL for Nominal GDP
API_URL = "https://api.worldbank.org/v2/country/US/indicator/NY.GDP.MKTP.CD?format=json&per_page=1000"

# Step 2: Fetch the data from the World Bank API
response = requests.get(API_URL)

if response.status_code == 200:
    data = response.json()
    if data and len(data) > 1:
        records = data[1]  # The first element contains metadata; the second contains data
        
        # Step 3: Parse the data into a DataFrame
        df = pd.DataFrame.from_records(records)
        
        # Keep relevant columns: date and value
        df = df[["date", "value"]]
        df.rename(columns={"date": "Year", "value": "Nominal GDP (Current US$)"}, inplace=True)
        
        # Drop rows with missing GDP values
        df.dropna(subset=["Nominal GDP (Current US$)"], inplace=True)
        
        # Convert GDP values to numeric
        df["Nominal GDP (Current US$)"] = pd.to_numeric(df["Nominal GDP (Current US$)"])
        
        # Sort by year in descending order
        df.sort_values(by="Year", ascending=False, inplace=True)
        
        # Step 4: Save to CSV
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
        os.makedirs(DATA_DIR, exist_ok=True)
        
        output_file = os.path.join(DATA_DIR, "us_nominal_gdp.csv")
        df.to_csv(output_file, index=False)
        print(f"Nominal GDP data saved to {output_file}")
    else:
        print("No data available in the response.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
