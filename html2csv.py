import csv
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

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

# Extract data for Manufacturing and Services PMI
manufacturing_file = "m_pmi.html"
services_file = "s_pmi.html"

manufacturing_data = extract_pmi_data(manufacturing_file)
services_data = extract_pmi_data(services_file)

# Save Manufacturing PMI to CSV
manufacturing_csv = "manufacturing_pmi.csv"
with open(manufacturing_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Date", "Actual", "Forecast", "Previous"])
    writer.writerows(manufacturing_data)

# Save Services PMI to CSV
services_csv = "services_pmi.csv"
with open(services_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Date", "Actual", "Forecast", "Previous"])
    writer.writerows(services_data)

# Load both datasets into Pandas DataFrames
df_manufacturing = pd.DataFrame(manufacturing_data, columns=["Date", "Actual", "Forecast", "Previous"])
df_manufacturing.set_index("Date", inplace=True)

df_services = pd.DataFrame(services_data, columns=["Date", "Actual", "Forecast", "Previous"])
df_services.set_index("Date", inplace=True)

# Plot Manufacturing and Services PMI
plt.figure(figsize=(14, 7))
plt.plot(df_manufacturing.index, df_manufacturing["Actual"], label="Manufacturing PMI", marker='o', color='b')
plt.plot(df_services.index, df_services["Actual"], label="Services PMI", marker='o', color='g')

# Filter x-axis labels for every two years
filtered_dates = df_manufacturing.index[df_manufacturing.index.year % 2 == 0].strftime("%Y").unique()
filtered_labels = [datetime.strptime(date, "%Y") for date in filtered_dates]
plt.xticks(filtered_labels, filtered_dates, rotation=45, fontsize=10)

# Adjust the plot
plt.xlabel("Year")
plt.ylabel("PMI")
plt.title("Manufacturing and Services PMI Over Time")
plt.legend()
plt.tight_layout()

# Save the plot
plot_file = "pmi_comparison_plot.png"
plt.savefig(plot_file)
print(f"Plot saved as {plot_file}")

# Show the plot
plt.show()
