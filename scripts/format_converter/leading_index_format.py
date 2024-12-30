import pandas as pd
import calendar

# Load the Unemployment Rate data
unemployment_rate_file_path = '/Users/jayjung/Desktop/dataset/Unemploymentrate.csv'
unemployment_rate_data = pd.read_csv(unemployment_rate_file_path)

# Reshape the data to have Year and OBS_VALUE columns
unemployment_rate_data_long = unemployment_rate_data.melt(
    id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
    var_name='Year',
    value_name='OBS_VALUE'
)

# Filter out rows where the Year column is not numeric (e.g., "Unnamed")
unemployment_rate_data_long = unemployment_rate_data_long[unemployment_rate_data_long['Year'].str.isdigit()]

# Filter data for years starting from 2000
unemployment_rate_data_long['Year'] = unemployment_rate_data_long['Year'].astype(int)
unemployment_rate_data_long = unemployment_rate_data_long[unemployment_rate_data_long['Year'] >= 2000]

# Generate all dates for each month and assign the OBS_VALUE to each day
expanded_rows = []

for _, row in unemployment_rate_data_long.iterrows():
    year = row['Year']
    obs_value = row['OBS_VALUE']
    for month in range(1, 13):
        days_in_month = calendar.monthrange(year, month)[1]
        for day in range(1, days_in_month + 1):
            expanded_rows.append({'Year': year, 'Month': month, 'Day': day, 'Unemployment_rate': obs_value})

# Create a new DataFrame with the expanded data
unemployment_rate_expanded = pd.DataFrame(expanded_rows)

# Save the expanded data to a CSV file
expanded_output_path = '/Users/jayjung/Desktop/dataset/UnemploymentRate_expanded.csv'
unemployment_rate_expanded.to_csv(expanded_output_path, index=False)

print("Expanded Unemployment Rate data has been saved to", expanded_output_path)
