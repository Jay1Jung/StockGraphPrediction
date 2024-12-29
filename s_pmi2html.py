from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time

# Step 1: Set up Selenium WebDriver
chrome_driver_path = os.path.expanduser("~/Documents/StockGraphPrediction/chromedriver-mac-x64/chromedriver")
service = Service(chrome_driver_path)

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
driver.set_page_load_timeout(180)

# Step 2: Open the URL
url = "https://www.investing.com/economic-calendar/services-pmi-1062"
driver.get(url)

# Step 3: Locate and click "Show More" until no more buttons
try:
    while True:
        try:
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()='Show more']"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
            driver.execute_script("arguments[0].click();", show_more_button)
            print("Clicked 'Show More' link.")
            time.sleep(2)
        except TimeoutException:
            print("No more 'Show More' links to click. Exiting loop.")
            break
except Exception as e:
    print(f"Error: {e}")

# Step 4: Remove the black section
try:
    black_section = driver.find_element(By.ID, "ad-container")
    driver.execute_script("arguments[0].remove();", black_section)
    print("Successfully removed ad section with ID 'ad-container'.")
except Exception as e:
    print(f"Failed to remove ad section: {e}")

# Step 5: Save the expanded table HTML
html_content = driver.page_source
with open("s_pmi.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("Successfully saved to 's_pmi.html'.")

# Step 6: Close the browser
driver.quit()
