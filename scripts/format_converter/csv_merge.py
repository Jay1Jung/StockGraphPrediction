import pandas as pd

# File paths
cpi_file = '/Users/jayjung/Desktop/dataset/CPI_expanded.csv'
dff_file = '/Users/jayjung/Desktop/dataset/DFF_transformed.csv'
gdp_file = '/Users/jayjung/Desktop/dataset/GDP_expanded.csv'
leading_index_file = '/Users/jayjung/Desktop/dataset/LeadingIndex_expanded.csv'
manufacturing_pmi_file = '/Users/jayjung/Desktop/dataset/manufacturing_pmi_transformed.csv'
services_pmi_file = '/Users/jayjung/Desktop/dataset/services_pmi_transformed.csv'
unemployment_rate_file = '/Users/jayjung/Desktop/dataset/UnemploymentRate_expanded.csv'
snp_file = "/Users/jayjung/Desktop/dataset/processed_sp500_data.csv"

# Load all datasets
cpi_data = pd.read_csv(cpi_file)
dff_data = pd.read_csv(dff_file)
gdp_data = pd.read_csv(gdp_file)
leading_index_data = pd.read_csv(leading_index_file)
manufacturing_pmi_data = pd.read_csv(manufacturing_pmi_file)
services_pmi_data = pd.read_csv(services_pmi_file)
unemployment_rate_data = pd.read_csv(unemployment_rate_file)
snp_closing_price = pd.read_csv(snp_file)

# Merge datasets on Year, Month, Day
merged_data = cpi_data

for data in [dff_data, gdp_data, leading_index_data, manufacturing_pmi_data, services_pmi_data, unemployment_rate_data, snp_closing_price]:
    merged_data = pd.merge(merged_data, data, on=['Year', 'Month', 'Day'], how='outer')

merged_data.rename(columns={
    'CPI_x': 'CPI',
    'DFF': 'DfF',
    'CPI_y' : "GDP", 
    'Actual_x': 'Manufacturing_PMI',
    'Actual_y': 'Services_PMI',
    'Unemployment_rate': 'Unemployment_Rate'
}, inplace=True)

# Save the merged dataset to a CSV file
output_path = '/Users/jayjung/Desktop/dataset/merged_data.csv'
merged_data.to_csv(output_path, index=False)

print("All datasets have been merged and saved to", output_path)