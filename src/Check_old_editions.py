from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

# Initialize WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open Diario Oficial Website
url = "https://www.boletinoficialdemineria.cl/?date=04-03-2025&edition=44090"
driver.get(url)

# Wait for the page to load
time.sleep(5)  # Increased sleep time to ensure page loads fully

# Get Page Source and Parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Look for the <a> with class 'lnkEdicionesAnteriores' (the correct link based on your inspection)
try:
    # Wait for the link to be clickable using Selenium
    wait = WebDriverWait(driver, 10)
    previous_editions_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.lnkEdicionesAnteriores p")))
    previous_editions_button.click()
    time.sleep(3)  # Allow the modal to appear
    print("✅ Clicked 'Ediciones Anteriores' and opened the pop-up")
except Exception as e:
    print(f"⚠️ Error: Could not click 'Ediciones Anteriores': {e}")

# For debugging purposes, do not save data to CSV right now, just to test
# Close WebDriver
driver.quit()
