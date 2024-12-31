from bs4 import BeautifulSoup
import csv
import os

# Prompt user to input the path of the HTML file
html_file_path = input("Enter the path to the HTML file: ")

# Check if the file exists
if not os.path.exists(html_file_path):
    print(f"Error: The file {html_file_path} does not exist.")
    exit(1)

# Load HTML content from the file
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_data = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_data, 'html.parser')
rows = soup.find_all('tr')

# Extract data and prepare for CSV
csv_data = []
for row in rows:
    cells = row.find_all('td')
    if len(cells) < 3:
        continue  # Skip rows that do not have enough columns
    
    date_cell = cells[0].get_text(strip=True)
    actual_value = cells[2].get_text(strip=True)

    # Parse the date (e.g., "Dec 11, 2024")
    try:
        month, day, year = date_cell.split()[:3]
        day = day.rstrip(',')  # Remove the comma from the day
    except ValueError:
        print(f"Skipping invalid date format: {date_cell}")
        continue

    # Append extracted data to the list
    csv_data.append([year, month, day, actual_value])

# Prompt user to specify output CSV file path
output_file = input("Enter the path to save the output CSV file: ")

# Ensure the directory exists
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save data to the specified CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Year', 'Month', 'Day', 'Actual'])  # Write the header
    writer.writerows(csv_data)  # Write the data

print(f"Data has been written to {output_file}")
