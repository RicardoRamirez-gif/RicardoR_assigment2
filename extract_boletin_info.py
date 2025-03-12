from playwright.sync_api import sync_playwright

def extract_boletin_info():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch browser
        page = browser.new_page()

        try:
            # Navigate to the URL and wait until the page is fully loaded
            page.goto("https://www.boletinoficialdemineria.cl/?date=11-03-2025&edition=44096", timeout=1200000)
            page.wait_for_load_state("networkidle")  # Wait for all network requests to finish

            # Extract the Boletín number, Date, and PDF link
            boletin_number = page.locator('.containerdate .alignleft').inner_text()
            date = page.locator('.containerdate .date strong').inner_text()
            pdf_link = page.locator('.containerdate .alignright a.summary').get_attribute('href')

            # Print extracted information
            print(f"Boletín Number: {boletin_number}")
            print(f"Date: {date}")
            print(f"PDF Link: {pdf_link}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

extract_boletin_info()
