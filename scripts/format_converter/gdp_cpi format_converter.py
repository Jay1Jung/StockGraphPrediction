import pandas as pd

# read file
file_path = '/Users/jayjung/Desktop/dataset/USA_CPI_filtered.csv'
data = pd.read_csv(file_path)

# extract the year
year_columns = [col for col in data.columns if col.isdigit()]

# create an array for monthly data
monthly_data = []

for year in year_columns:
    year_data = pd.DataFrame({
        'Year': [int(year)] * 12,
        'Month': list(range(1, 13)),
        'GDP': [float(data[year])] * 12  
    })
    monthly_data.append(year_data)

# concat all the monthly information
monthly_data_df = pd.concat(monthly_data, ignore_index=True)

# saving the information
output_file_path = '/Users/jayjung/Desktop/dataset/USA_CPI_monthly.csv'
monthly_data_df.to_csv(output_file_path, index=False)

print("unification success")