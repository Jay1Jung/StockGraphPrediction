import pandas as pd

# Load the DFF data
dff_file_path = '/Users/jayjung/Desktop/dataset/DFF.csv'
dff_data = pd.read_csv(dff_file_path)

# Split the observation_date into Year, Month, and Day
dff_data['Year'] = pd.to_datetime(dff_data['observation_date']).dt.year
dff_data['Month'] = pd.to_datetime(dff_data['observation_date']).dt.month
dff_data['Day'] = pd.to_datetime(dff_data['observation_date']).dt.day

# Rearrange columns to have Year, Month, Day, and DFF
dff_data_transformed = dff_data[['Year', 'Month', 'Day', 'DFF']]

# Save the transformed data to a CSV file
output_path = '/Users/jayjung/Desktop/dataset/DFF_transformed.csv'
dff_data_transformed.to_csv(output_path, index=False)

print("DFF data has been transformed and saved to", output_path)