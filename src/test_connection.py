from playwright.sync_api import sync_playwright

def test_connection():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  
        page = browser.new_page()
        
        try:
            # Increase timeout significantly
            page.goto("https://www.boletinoficialdemineria.cl/?date=11-03-2025&edition=44096", timeout=90000)  # 90 seconds
            page.wait_for_load_state("load")  # Wait for the page to fully load
            print("Page Title:", page.title())  # Print the title after the page is loaded
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

test_connection()
