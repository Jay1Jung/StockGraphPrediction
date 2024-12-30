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

# Set up paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DRIVERS_DIR = os.path.join(PROJECT_ROOT, "drivers")
CHROMEDRIVER_PATH = os.path.join(DRIVERS_DIR, "chromedriver-mac-x64", "chromedriver")
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)
CPI_HTML_FILE = os.path.join(RAW_DATA_DIR, "us_cpi_table.html")

# Set up Selenium WebDriver
service = Service(CHROMEDRIVER_PATH)

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-images")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-extensions")
options.add_argument("--disable-software-rasterizer")
options.add_argument("start-maximized")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(300)

# Open the URL
url = "https://www.investing.com/economic-calendar/cpi-733"
try:
    driver.get(url)

    # Wait for the table to load
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "eventHistoryTable733"))
    )
    print("Table loaded successfully.")

    # Expand the "Show More" sections
    while True:
        try:
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()='Show more']"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
            driver.execute_script("arguments[0].click();", show_more_button)
            time.sleep(2)
        except TimeoutException:
            print("No more 'Show More' buttons to click.")
            break

    # Extract the table
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", {"id": "eventHistoryTable733"})

    if table:
        with open(CPI_HTML_FILE, "w", encoding="utf-8") as file:
            file.write(str(table))
        print(f"Extracted CPI table saved to '{CPI_HTML_FILE}'.")
    else:
        print("Error: Table with id 'eventHistoryTable733' not found.")
finally:
    driver.quit()
