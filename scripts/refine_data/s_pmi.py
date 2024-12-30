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
os.makedirs(PLOTS_DIR, exist_ok=True)

# File paths
services_file = os.path.join(RAW_DATA_DIR, "s_pmi_table.html")
services_csv = os.path.join(PROCESSED_DATA_DIR, "services_pmi.csv")
services_plot = os.path.join(PLOTS_DIR, "services_pmi_plot.png")


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
        if len(cols) > 2:
            date = cols[0]
            actual = cols[2]
            forecast = cols[3]
            previous = cols[4]

            try:
                parsed_date = datetime.strptime(date.split('(')[0].strip(), "%b %d, %Y")
                actual_value = float(actual)
                forecast_value = float(forecast) if forecast else None
                previous_value = float(previous) if previous else None
                data.append([parsed_date, actual_value, forecast_value, previous_value])
            except ValueError:
                pass

    return data


# Extract data
services_data = extract_pmi_data(services_file)

# Save to CSV
with open(services_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Date", "Actual", "Forecast", "Previous"])
    writer.writerows(services_data)

# Load data into DataFrame
df_services = pd.DataFrame(services_data, columns=["Date", "Actual", "Forecast", "Previous"])
df_services.set_index("Date", inplace=True)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(df_services.index, df_services["Actual"], label="Services PMI", marker='o', color='g')
plt.xlabel("Year")
plt.ylabel("PMI")
plt.title("Services PMI Over Time")
plt.legend()
plt.tight_layout()

# Save the plot
plt.savefig(services_plot)
print(f"Services PMI plot saved as {services_plot}")
