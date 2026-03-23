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
options = Options()
options.add_argument("--headless")  # Required for Termux/No-GUI environments

options.set_preference("general.useragent.override",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

options.set_preference("dom.webdriver.enabled", False)
options.set_preference("useAutomationExtension", False)

def get_final_price(url):
    prices = {}
    prices["url"] = url
    
    driver = None

    try:
        print(f"Launching Firefox to scrape: {url}")
        driver = webdriver.Firefox(service=service, options=options)
        wait = WebDriverWait(driver, 600)
                
        driver.get(url)
        time.sleep(3)

        title = driver.title
        prices["title"] = title
        print(f"Page Title: {driver.title}")

        price_elem = wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "pdp-v2-product-price-content-salePrice-amount")
            )
        )

        price_text = price_elem.text.strip()
        cleaned = price_text.replace(",", "")
        match = re.search(r"[\d,\.]+", cleaned)  # remove \ escape from \d
        if match:
            num_str = match.group()
            final_price = float(num_str)
            prices["final_price"] = f"${final_price}"
            return prices
        else:
            raise ValueError(f"Could not parse price from '{price_text}'")

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

    prices = get_final_price(url)

    print(f"URL: {prices.get('url', 'N/A')}")
    print(f"Title: {prices.get('title', 'N/A')}")
    print(f"🎯 Price: {prices.get('final_price', 'N/A')}")
