import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

# -----------------------------
# 🧹 CLEAN UP OLD PROCESSES
# -----------------------------
os.system("pkill -f chromedriver")
os.system("pkill -f chromium")

# -----------------------------
# ⚙️ CHROME OPTIONS (TERMUX SAFE)
# -----------------------------
options = Options()

# Set correct binary path (IMPORTANT)
options.binary_location = "/data/data/com.termux/files/usr/bin/chromium-browser"

options.page_load_strategy = "eager"

# Stability flags (VERY IMPORTANT in Termux)
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")

# Speed optimization (disable images)
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

# -----------------------------
# 🚗 CHROMEDRIVER PATH
# -----------------------------
service = Service("/data/data/com.termux/files/usr/bin/chromedriver")

# -----------------------------
# 🚀 START DRIVER
# -----------------------------
try:
    driver = webdriver.Chrome(service=service, options=options)

    # Increase timeouts
    driver.set_page_load_timeout(120)
    driver.set_script_timeout(120)

    print("✅ Driver started successfully")

    # -----------------------------
    # 🌐 OPEN WEBSITE
    # -----------------------------
    url = "http://www.yahoo.com"
    print(f"Opening: {url}")

    try:
        driver.get(url)
    except TimeoutException:
        print("⚠️ Page load timed out, continuing...")

    # Wait for content
    time.sleep(5)

    # -----------------------------
    # 📄 SCRAPE DATA
    # -----------------------------
    print("Page title:", driver.title)

    links = driver.find_elements("tag name", "a")
    print(f"Found {len(links)} links")

    for link in links[:5]:  # print first 5 links only
        print(link.text, "->", link.get_attribute("href"))

# -----------------------------
# ❌ ERROR HANDLING
# -----------------------------
except Exception as e:
    print("❌ ERROR:", e)

# -----------------------------
# 🛑 CLEAN EXIT (VERY IMPORTANT)
# -----------------------------
finally:
    try:
        driver.quit()
        print("🛑 Driver closed")
    except:
        pass

    # Extra cleanup (force kill if needed)
    os.system("pkill -f chromedriver")
    os.system("pkill -f chromium")
