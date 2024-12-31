import pandas as pd
import os


def process_files(folder_path, output_file):
    merged_data = pd.DataFrame()

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if "CPI" in file_name:
            df = pd.read_csv(file_path)
            df = df.rename(columns={"Actual": "CPI"})
            merged_data = pd.concat([merged_data, df], ignore_index=True, axis=0)

        elif "DFF" in file_name:
            df = pd.read_csv(file_path)
            merged_data = pd.merge(merged_data, df, on=["Year", "Month", "Day"], how="outer")

        elif "GDP" in file_name:
            df = pd.read_csv(file_path)
            merged_data = pd.merge(merged_data, df, on=["Year", "Month", "Day"], how="outer")

        elif "Leading_index" in file_name:
            df = pd.read_csv(file_path)
            df = df.rename(columns={"Actual": "Leading_Index"})
            merged_data = pd.merge(merged_data, df, on=["Year", "Month", "Day"], how="outer")

        elif "manufacturing_pmi" in file_name:
            df = pd.read_csv(file_path)
            df["Date"] = pd.to_datetime(df["Date"])
            df["Year"] = df["Date"].dt.year
            df["Month"] = df["Date"].dt.month
            df["Day"] = df["Date"].dt.day
            df = df.rename(columns={"Actual": "Manufacturing_PMI"})
            df = df[["Year", "Month", "Day", "Manufacturing_PMI"]]
            merged_data = pd.merge(merged_data, df, on=["Year", "Month", "Day"], how="outer")

        elif "services_pmi" in file_name:
            df = pd.read_csv(file_path)
            df["Date"] = pd.to_datetime(df["Date"])
            df["Year"] = df["Date"].dt.year
            df["Month"] = df["Date"].dt.month
            df["Day"] = df["Date"].dt.day
            df = df.rename(columns={"Actual": "Services_PMI"})
            df = df[["Year", "Month", "Day", "Services_PMI"]]
            merged_data = pd.merge(merged_data, df, on=["Year", "Month", "Day"], how="outer")

        elif "sp500_data" in file_name:
            df = pd.read_csv(file_path)
            df["Date"] = pd.to_datetime(df["Date"])
            df["Year"] = df["Date"].dt.year
            df["Month"] = df["Date"].dt.month
            df["Day"] = df["Date"].dt.day
            df = df.rename(columns={"Close": "SP500_Close"})
            df = df[["Year", "Month", "Day", "SP500_Close"]]
            merged_data = pd.merge(merged_data, df, on=["Year", "Month", "Day"], how="outer")

        elif "UnemploymentRate" in file_name:
            df = pd.read_csv(file_path)
            extracted_dates = df["Release Date"].str.extract(r"(?P<Month>[A-Za-z]{3}) (?P<Day>\d+), (?P<Year>\d+)")
            extracted_dates.dropna(inplace=True)
            extracted_dates["Month"] = pd.to_datetime(extracted_dates["Month"], format="%b").dt.month
            extracted_dates["Day"] = extracted_dates["Day"].astype(int)
            extracted_dates["Year"] = extracted_dates["Year"].astype(int)
            df = pd.concat([df, extracted_dates], axis=1)
            df = df.rename(columns={"Actual": "Unemployment_Rate"})
            df = df[["Year", "Month", "Day", "Unemployment_Rate"]]
            merged_data = pd.merge(merged_data, df, on=["Year", "Month", "Day"], how="outer")

    merged_data.fillna(method="ffill", inplace=True)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    if not os.path.exists(output_file):
        with open(output_file, 'w') as f:
            pass

    merged_data.to_csv(output_file, index=False)
    print(f"Merged data has been saved to {output_file}")


if __name__ == "__main__":
    folder_path = input("Enter the folder path containing the CSV files: ").strip()
    output_file = input("Enter the output file path: ").strip()

    if not os.path.exists(folder_path):
        print(f"Error: The folder {folder_path} does not exist.")
    else:
        try:
            process_files(folder_path, output_file)
        except Exception as e:
            print(f"An error occurred: {e}")
