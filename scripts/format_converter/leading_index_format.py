import pandas as pd

file_path = '/Users/jayjung/Desktop/dataset/USA_Leading_Index_Converted.csv'
data = pd.read_csv(file_path)

# split year and month
data[['Year', 'Month']] = data['TIME_PERIOD'].str.split('-', expand=True)

# convert data type
data['Year'] = data['Year'].astype(int)
data['Month'] = data['Month'].astype(int)

transformed_data = data[['Year', 'Month', 'OBS_VALUE']]


# save the information.
output_file_path = '/Users/jayjung/Desktop/dataset/USA_Leading_Index_Separated.csv'
transformed_data.to_csv(output_file_path, index=False)

# print the result.
print("coversion success")