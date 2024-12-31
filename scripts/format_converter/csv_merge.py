import pandas as pd
import os

def load_and_merge_datasets(base_dir):
    """Load and merge datasets from the specified directory."""
    # File names relative to the base directory
    files = {
        "cpi_file": "CPI_expanded.csv",
        "dff_file": "DFF_transformed.csv",
        "gdp_file": "GDP_expanded.csv",
        "leading_index_file": "LeadingIndex_expanded.csv",
        "manufacturing_pmi_file": "manufacturing_pmi.csv",
        "services_pmi_file": "services_pmi.csv",
        "unemployment_rate_file": "UnemploymentRate.csv",
        "snp_file": "sp500_data.csv"
    }

    # Load datasets
    datasets = {}
    for name, file in files.items():
        file_path = os.path.join(base_dir, file)
        if os.path.exists(file_path):
            datasets[name] = pd.read_csv(file_path)
        else:
            print(f"Warning: {file} not found at {file_path}. Skipping...")
            datasets[name] = pd.DataFrame()  # Placeholder for missing data

    # Merge datasets on Year, Month, Day
    merged_data = datasets["cpi_file"]

    for key, data in datasets.items():
        if not data.empty:
            merged_data = pd.merge(merged_data, data, on=['Year', 'Month', 'Day'], how='outer')

    # Rename columns
    merged_data.rename(columns={
        'CPI_x': 'CPI',
        'DFF': 'DfF',
        'CPI_y': 'GDP',
        'Actual_x': 'Manufacturing_PMI',
        'Actual_y': 'Services_PMI',
        'Unemployment_rate': 'Unemployment_Rate'
    }, inplace=True, errors="ignore")  # Avoid errors if columns don't exist

    # Handle missing values (optional)
    merged_data.fillna(method='ffill', inplace=True)  # Forward fill missing values

    return merged_data


def main():
    # Prompt the user to specify the data directory
    base_dir = input("Enter the base directory for datasets (default is './data/raw'): ").strip()
    if not base_dir:
        base_dir = './data/raw'

    if not os.path.exists(base_dir):
        print(f"Error: The specified directory '{base_dir}' does not exist.")
        return

    try:
        merged_data = load_and_merge_datasets(base_dir)
        output_path = os.path.join(base_dir, 'merged_data.csv')
        merged_data.to_csv(output_path, index=False)
        print(f"All datasets have been merged and saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()