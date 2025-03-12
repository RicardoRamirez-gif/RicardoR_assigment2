from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import pandas as pd

# Initialize WebDriver
options = webdriver.ChromeOptions()
# Remove "--headless" for debugging (try running without headless mode first)
# options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open Diario Oficial Website
url = "https://www.boletinoficialdemineria.cl/?date=11-03-2025&edition=44096"
driver.get(url)

try:
    # Wait for "Ediciones Anteriores" button to be clickable
    wait = WebDriverWait(driver, 10)
    previous_editions_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Ediciones Anteriores')]")))
    previous_editions_button.click()
    time.sleep(3)  # Allow modal to appear
except Exception as e:
    print(f"⚠️ Error: Could not click 'Ediciones Anteriores': {e}")

# Get Page Source and Parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find all historical editions
boletins = []
for item in soup.select("div[data-date] a"):
    href = item.get("href", "")
    if "?date=" in href and "&edition=" in href:
        date = href.split("?date=")[-1].split("&")[0]  # Extract date
        edition = href.split("&edition=")[-1]  # Extract edition number
        link = f"https://www.boletinoficialdemineria.cl{href}"  # Construct full link

        boletins.append({"Date": date, "Boletin Number": edition, "PDF Link": link})

# Save Data to CSV
df = pd.DataFrame(boletins)
df.to_csv("boletins.csv", index=False)
print("✅ Data saved to 'boletins.csv'")

# Close WebDriver
driver.quit()
