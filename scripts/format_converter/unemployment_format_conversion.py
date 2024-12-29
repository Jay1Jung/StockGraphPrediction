import pandas as pd

# Read the unemployment data file
file_path = '/Users/jayjung/Desktop/dataset/USA_Unemployment_filtered.csv'
data = pd.read_csv(file_path)

# Extract numeric year columns
year_columns = [col for col in data.columns if col.isdigit()]

# Convert data to monthly format
monthly_data = []
for year in year_columns:
    if not data[year].isnull().all():  # Skip years with all NaN values
        year_data = pd.DataFrame({
            'Year': [int(year)] * 12,
            'Month': list(range(1, 13)),
            'Unemployment Rate': [data[year].iloc[0]] * 12  # Repeat the annual value for 12 months
        })
        monthly_data.append(year_data)

# Combine all years into a single DataFrame
monthly_data_df = pd.concat(monthly_data, ignore_index=True)

# Save the transformed data
output_file_path = '/Users/jayjung/Desktop/dataset/USA_Unemployment_Monthly_Transformed.csv'
monthly_data_df.to_csv(output_file_path, index=False)

print(f"Transformed file saved: {output_file_path}")