import os
import csv
from bs4 import BeautifulSoup

# Set up dynamic paths
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

# Ensure the directories exist (usually they do, but just in case)
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# File paths
html_file_path = os.path.join(RAW_DATA_DIR, "us_cpi_table.html")  # Adjust name if needed
output_file = os.path.join(PROCESSED_DATA_DIR, "us_cpi.csv")      # Adjust name if needed

# 3. Check that the HTML file exists
if not os.path.exists(html_file_path):
    print(f"Error: The file '{html_file_path}' does not exist.")
    exit(1)

# 4. Parse the HTML file using BeautifulSoup
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_data = file.read()

soup = BeautifulSoup(html_data, 'html.parser')
rows = soup.find_all('tr')

# 5. Extract data (date + actual_value) from rows
csv_data = []
for row in rows:
    cells = row.find_all('td')
    # Ensure we have enough cells in the row
    if len(cells) < 3:
        continue
    
    # Example data:
    #   td 1: date like "Dec 11, 2024"
    #   td 2: something else (we skip)
    #   td 3: actual value
    date_cell = cells[0].get_text(strip=True)
    actual_value = cells[2].get_text(strip=True)
    
    # Parse the date (assuming format "Dec 11, 2024")
    try:
        month, day, year = date_cell.split()[:3]
        day = day.rstrip(',')  # remove trailing comma from day
    except ValueError:
        print(f"Skipping invalid date format: {date_cell}")
        continue

    csv_data.append([year, month, day, actual_value])

# 6. Write the extracted data to CSV (no user prompt)
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)

with open(output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Year', 'Month', 'Day', 'Actual'])  # CSV header
    writer.writerows(csv_data)  # CSV data rows

print(f"Data has been written to: {output_file}")
