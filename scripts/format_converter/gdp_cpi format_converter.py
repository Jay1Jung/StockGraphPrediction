import pandas as pd
import calendar

# Load the CPI data
cpi_file_path = '/Users/jayjung/Desktop/dataset/GDP.csv'
cpi_data = pd.read_csv(cpi_file_path)

# Reshape the CPI data to have Year and CPI columns
cpi_long_format = cpi_data.melt(
    id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
    var_name='Year',
    value_name='GDP'
)

# Filter out rows where the Year column is not numeric (e.g., "Unnamed")
cpi_long_format = cpi_long_format[cpi_long_format['Year'].str.isdigit()]

# Filter the data for years starting from 2000
cpi_filtered = cpi_long_format[cpi_long_format['Year'].astype(int) >= 2000].copy()

# Generate all dates for each year and month with their respective CPI values
expanded_rows = []

for _, row in cpi_filtered.iterrows():
    year = int(row['Year'])
    cpi_value = row['GDP']
    for month in range(1, 13):
        # Get the number of days in the month
        days_in_month = calendar.monthrange(year, month)[1]
        for day in range(1, days_in_month + 1):
            expanded_rows.append({'Year': year, 'Month': month, 'Day': day, 'CPI': cpi_value})

# Create a new DataFrame with the expanded data
cpi_expanded = pd.DataFrame(expanded_rows)

# Save the expanded data to a CSV file
expanded_output_path = '/Users/jayjung/Desktop/dataset/GDP_expanded.csv'
cpi_expanded.to_csv(expanded_output_path, index=False)

print("Expanded GDP data has been saved to", expanded_output_path)