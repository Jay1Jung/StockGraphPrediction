import os
import pandas as pd

folder_path ='/Users/jayjung/Desktop/dataset'

csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

gdp_data = pd.read_csv(os.path.join(folder_path, 'USA_GDP_monthly.csv'))
cpi_data = pd.read_csv(os.path.join(folder_path, 'USA_CPI_monthly.csv'))
unemployment_data = pd.read_csv(os.path.join(folder_path, 'USA_Unemployment_monthly.csv'))
federal_funds_data = pd.read_csv(os.path.join(folder_path, 'Federal_Funds_Monthly_Averages.csv'))
leading_index_data = pd.read_csv(os.path.join(folder_path, 'USA_Leading_Index_Separated.csv' ))

# merging data
merged_data = gdp_data.merge(cpi_data, on=['Year', 'Month'], how='outer', suffixes=('', '_CPI'))
merged_data = merged_data.merge(unemployment_data, on=['Year', 'Month'], how='outer', suffixes=('', '_Unemployment'))
merged_data = merged_data.merge(federal_funds_data, on=['Year', 'Month'], how='outer', suffixes=('', '_FedFunds'))
merged_data = merged_data.merge(leading_index_data, on=['Year', 'Month'], how ='outer', suffixes=('', '_LeadIndex'))

# renaming the rows
merged_data.rename(columns={
    'GDP': 'GDP',
    'GDP_CPI': 'CPI',
    'Unemployment Rate': 'Unemployment_Rate',
    'Average Rate': 'Federal_Funds_Rate',
    'OBS_VALUE' : 'Leading_index'


}, inplace=True)

# save the result
output_file_path = '/Users/jayjung/Desktop/dataset/merged_data.csv'
merged_data.to_csv(output_file_path, index=False)

print(f"All datasets merged and saved to: {output_file_path}")