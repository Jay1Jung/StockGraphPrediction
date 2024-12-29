import pandas as pd

# Load the federal funds data
file_path = '/Users/jayjung/Desktop/dataset/Federal funds Effective Rate.csv'
data = pd.read_csv(file_path)

# Convert observation_date to datetime
data['observation_date'] = pd.to_datetime(data['observation_date'])

# Extract Year and Month
data['Year'] = data['observation_date'].dt.year
data['Month'] = data['observation_date'].dt.month

# Group by Year and Month and calculate the monthly average rate
monthly_data = data.groupby(['Year', 'Month'], as_index=False)['DFF'].mean()
monthly_data.rename(columns={'DFF': 'Average Rate'}, inplace=True)

# Save the transformed data
output_file_path = '/Users/jayjung/Desktop/dataset/Federal_Funds_Monthly_Averages.csv'
monthly_data.to_csv(output_file_path, index=False)

print(f"Transformed file saved: {output_file_path}")