from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time

# 1. Setup Firefox Options
options = Options()
options.add_argument("--headless")  # Required for Termux/No-GUI environments

# 2. Define the Service (Points to the geckodriver installed by pkg)
# In Termux, geckodriver is usually at /data/data/com.termux/files/usr/bin/geckodriver
service = Service("/data/data/com.termux/files/usr/bin/geckodriver")

def scrape_site(url):
    driver = None
    try:
        print(f"Launching Firefox to scrape: {url}")
        driver = webdriver.Firefox(service=service, options=options)
        
        # Navigate to the site
        driver.get(url)
        
        # Give the page time to load JavaScript (if necessary)
        time.sleep(3)
        
        # Example: Get the page title
        print(f"Page Title: {driver.title}")
        
        # Example: Extract all text from <h1> tags
        h1_elements = driver.find_elements("tag name", "h1")
        for idx, tag in enumerate(h1_elements):
            print(f"Heading {idx+1}: {tag.text}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()
            print("Browser closed.")

if __name__ == "__main__":
    target_url = "https://www.google.com"  # Replace with your target
    scrape_site(target_url)
