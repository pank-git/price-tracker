import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

geckodriver_path = "/data/data/com.termux/files/usr/bin/geckodriver"

service = Service(geckodriver_path)
options = webdriver.ChromeOptions()

options = Options()
options.add_argument("--headless")  # Required for Termux/No-GUI environments

def get_final_price(url):
    prices = {}
    prices["url"] = url
    
    driver = None

    try:
        print(f"Launching Firefox to scrape: {url}")
        driver = webdriver.Firefox(service=service, options=options)
        wait = WebDriverWait(driver, 120)
                
        driver.get(url)
        time.sleep(3)

        title = driver.title
        prices["title"] = title
        print(f"Page Title: {driver.title}")

        time.sleep(30)

        html = driver.page_source
        
        matches = re.findall(r".{0,50}719.{0,50}", html)
        
        for m in matches:
            print(m)

       

    except Exception as e:
        print(f"💥 STEP ERROR: Unhandled exception in get_final_price:")
        print(f"  {type(e).__name__}: {e}")
        raise e

    finally:
        if driver:
            driver.quit()
            print("Browser closed.")


if __name__ == "__main__":
    url = "https://www.lazada.sg/products/2025-new-xiaomi-pad-8-pro-series-tablet-snapdragon-8-elite-xiaomi-pad-8-tablet-snapdragon-8s-gen-4-112inchs-32k-144hz-lcd-screen-9200mah-67w-fastcharge-xiaomi-tablet-i3549288820-s23434820718.html"
    get_final_price(url)
  
