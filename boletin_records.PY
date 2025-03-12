import csv
import os
from playwright.sync_api import sync_playwright

# File path for storing boletin records
CSV_FILE = "boletin_records.csv"

def extract_boletin_info():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Navigate to the URL and wait until the page is fully loaded
            url = "https://www.boletinoficialdemineria.cl/?date=11-03-2025&edition=44096"
            page.goto(url, timeout=1200000)
            page.wait_for_load_state("networkidle")  # Ensure all network requests are complete

            # Extract information
            boletin_number = page.locator('.containerdate .alignleft').inner_text().strip()
            date = page.locator('.containerdate .date strong').inner_text().strip()
            pdf_link = page.locator('.containerdate .alignright a.summary').get_attribute('href')

            # Print extracted information
            print(f"Boletín Number: {boletin_number}")
            print(f"Date: {date}")
            print(f"PDF Link: {pdf_link}")

            # Save to CSV
            save_to_csv([boletin_number, date, pdf_link])

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

def save_to_csv(data):
    """Appends extracted data to a CSV file, creating one if it doesn't exist."""
    file_exists = os.path.isfile(CSV_FILE)
    
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header if file does not exist
        if not file_exists:
            writer.writerow(["Boletín Number", "Date", "PDF Link"])
        
        writer.writerow(data)
        print(f"Record saved to {CSV_FILE}")

if __name__ == "__main__":
    extract_boletin_info()
