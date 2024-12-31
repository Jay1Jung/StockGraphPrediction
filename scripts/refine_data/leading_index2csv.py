import os
import csv
from bs4 import BeautifulSoup

# 1. Determine project paths
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

# 2. Define input/output files
leading_index_html_path = os.path.join(RAW_DATA_DIR, "us_leading_index_table.html")
leading_index_csv_path = os.path.join(PROCESSED_DATA_DIR, "us_leading_index.csv")

# 3. Ensure the input file exists
if not os.path.exists(leading_index_html_path):
    print(f"Error: The file '{leading_index_html_path}' does not exist.")
    exit(1)

# 4. Read the HTML and parse with BeautifulSoup
with open(leading_index_html_path, 'r', encoding='utf-8') as file:
    html_data = file.read()

soup = BeautifulSoup(html_data, 'html.parser')
rows = soup.find_all('tr')

# 5. Extract data into a list for CSV
#    Assuming first <td> is date, and third <td> is the leading index value.
csv_data = []
for row in rows:
    cells = row.find_all('td')
    if len(cells) < 3:
        continue  # skip any row with fewer than 3 columns
    
    # Example date format: "Dec 11, 2024"
    date_text = cells[0].get_text(strip=True)
    leading_value = cells[2].get_text(strip=True)
    
    try:
        month, day, year = date_text.split()[:3]
        day = day.rstrip(',')  # remove comma (e.g. "11," -> "11")
    except ValueError:
        # If the date doesn't match the expected format, skip
        continue
    
    csv_data.append([year, month, day, leading_value])

# 6. Ensure output directory exists
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# 7. Write to CSV (overwrite or append—your choice).
#    Below, we always overwrite the file with the newest results.
with open(leading_index_csv_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write a header row
    writer.writerow(["Year", "Month", "Day", "LeadingIndex"])
    # Write the extracted data
    writer.writerows(csv_data)

print(f"Leading index data has been written to '{leading_index_csv_path}'")
