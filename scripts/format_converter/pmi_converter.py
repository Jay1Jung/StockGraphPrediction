import pandas as pd

# Load the services PMI data
services_pmi_file_path = '/Users/jayjung/Desktop/dataset/manufacturing_pmi.csv'
services_pmi_data = pd.read_csv(services_pmi_file_path)

# Convert the Date column to datetime format
services_pmi_data['Date'] = pd.to_datetime(services_pmi_data['Date'])

# Extract Year, Month, and Day from the Date column
services_pmi_data['Year'] = services_pmi_data['Date'].dt.year
services_pmi_data['Month'] = services_pmi_data['Date'].dt.month
services_pmi_data['Day'] = services_pmi_data['Date'].dt.day

# Rearrange columns to have Year, Month, Day, and Actual PMI values
services_pmi_transformed = services_pmi_data[['Year', 'Month', 'Day', 'Actual']]

# Save the transformed data to a CSV file
output_path = '/Users/jayjung/Desktop/dataset/manufacturing_pmi_transformed.csv'
services_pmi_transformed.to_csv(output_path, index=False)

print("Services PMI data has been transformed and saved to", output_path)
