import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time

# Step 1: Set up paths dynamically
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))  # Two levels up from this file
DRIVERS_DIR = os.path.join(PROJECT_ROOT, "drivers")
CHROMEDRIVER_PATH = os.path.join(DRIVERS_DIR, "chromedriver-mac-x64", "chromedriver")
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)
UNEMPLOYMENT_HTML_FILE = os.path.join(RAW_DATA_DIR, "unemployment_rate_table.html")

# Step 2: Set up Selenium WebDriver
service = Service(CHROMEDRIVER_PATH)

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("start-maximized")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(300)

# Step 3: Open the URL
url = "https://www.investing.com/economic-calendar/unemployment-rate-300"
try:
    driver.get(url)

    # Step 4: Locate and click "Show More" until no more buttons
    while True:
        try:
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()='Show more']"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
            driver.execute_script("arguments[0].click();", show_more_button)
            time.sleep(2)  # Allow time for content to load
        except TimeoutException:
            print("No more 'Show More' links to click.")
            break

    # Step 5: Extract the desired table using BeautifulSoup
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", {"id": "eventHistoryTable300"})

    if table:
        # Save the extracted table as a standalone HTML file
        with open(UNEMPLOYMENT_HTML_FILE, "w", encoding="utf-8") as file:
            file.write(str(table))
        print(f"Extracted Unemployment Rate table saved to '{UNEMPLOYMENT_HTML_FILE}'.")
    else:
        print("Error: Table with id 'eventHistoryTable300' not found.")
finally:
    driver.quit()
