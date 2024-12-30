import os
import csv
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# Set up dynamic paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
PLOTS_DIR = os.path.join(PROJECT_ROOT, "plots")
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# File paths
manufacturing_file = os.path.join(RAW_DATA_DIR, "m_pmi_table.html")
manufacturing_csv = os.path.join(PROCESSED_DATA_DIR, "manufacturing_pmi.csv")
manufacturing_plot = os.path.join(PLOTS_DIR, "manufacturing_pmi_plot.png")

def extract_pmi_data(file_path):
    """Extract PMI data (Date, Actual, Forecast, Previous) from an HTML file."""
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <tr> tags with ids that start with "historicEvent_"
    rows = soup.find_all("tr", id=lambda x: x and x.startswith("historicEvent_"))

    # Prepare the data
    data = []
    for row in rows:
        cols = [col.text.strip() for col in row.find_all("td")]
        if len(cols) > 2:  # Ensure there is enough data
            date = cols[0]  # Extract Date
            actual = cols[2]  # Extract Actual
            forecast = cols[3]  # Extract Forecast
            previous = cols[4]  # Extract Previous

            # Parse and append data
            try:
                parsed_date = datetime.strptime(date.split('(')[0].strip(), "%b %d, %Y")
                actual_value = float(actual)
                forecast_value = float(forecast) if forecast else None
                previous_value = float(previous) if previous else None
                data.append([parsed_date, actual_value, forecast_value, previous_value])
            except ValueError:
                pass  # Skip rows with invalid values

    return data

# Extract data
manufacturing_data = extract_pmi_data(manufacturing_file)

# Save Manufacturing PMI to CSV
with open(manufacturing_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Date", "Actual", "Forecast", "Previous"])
    writer.writerows(manufacturing_data)

# Load both datasets into Pandas DataFrames
df_manufacturing = pd.DataFrame(manufacturing_data, columns=["Date", "Actual", "Forecast", "Previous"])
df_manufacturing.set_index("Date", inplace=True)

# Plot Manufacturing 
plt.figure(figsize=(14, 7))
plt.plot(df_manufacturing.index, df_manufacturing["Actual"], label="Manufacturing PMI", marker='o', color='b')
plt.xlabel("Year")
plt.ylabel("PMI")
plt.title("Manufacturing and Services PMI Over Time")
plt.legend()
plt.tight_layout()

# Save the plot
plt.savefig(manufacturing_plot)
print(f"Manufacturing PMI Plot saved as {manufacturing_plot}")