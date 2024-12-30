import pandas as pd
import calendar

# Load the Unemployment Rate data
unemployment_rate_file_path = '/Users/jayjung/Desktop/dataset/Unemploymentrate.csv' 
unemployment_rate_data = pd.read_csv(unemployment_rate_file_path)

# Extract Year and Month from the TIME_PERIOD column
unemployment_rate_data['Year'] = unemployment_rate_data['TIME_PERIOD'].str[:4].astype(int)
unemployment_rate_data['Month'] = unemployment_rate_data['TIME_PERIOD'].str[5:7].astype(int)

# Filter data for years starting from 2000
unemployment_rate_data = unemployment_rate_data[unemployment_rate_data['Year'] >= 2000]

# Generate all dates for each month and assign the OBS_VALUE to each day
expanded_rows = []

for _, row in unemployment_rate_data.iterrows():
    year = row['Year']
    month = row['Month']
    obs_value = row['OBS_VALUE']
    days_in_month = calendar.monthrange(year, month)[1]
    for day in range(1, days_in_month + 1):
        expanded_rows.append({'Year': year, 'Month': month, 'Day': day, 'OBS_VALUE': obs_value})

# Create a new DataFrame with the expanded data
unemployment_rate_expanded = pd.DataFrame(expanded_rows)

# Save the expanded data to a CSV file
expanded_output_path = 'UnemploymentRate_expanded.csv'
unemployment_rate_expanded.to_csv(expanded_output_path, index=False)

print("Expanded Unemployment Rate data has been saved to", expanded_output_path)