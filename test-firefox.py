import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -----------------------------
# 🧹 CLEAN UP OLD PROCESSES
# -----------------------------
os.system("pkill -f geckodriver")
os.system("pkill -f firefox")

# -----------------------------
# ⚙️ FIREFOX OPTIONS (TERMUX SAFE)
# -----------------------------
options = Options()
options.headless = True  # run in background

# Reduce resource usage
options.set_preference("permissions.default.image", 2)  # disable images
options.set_preference("dom.ipc.processCount", 1)       # single process
options.set_preference("browser.shell.checkDefaultBrowser", False)

# -----------------------------
# 🚗 GECKODRIVER PATH
# -----------------------------
service = Service("/data/data/com.termux/files/usr/bin/geckodriver")

# -----------------------------
# 🚀 START DRIVER
# -----------------------------
try:
    driver = webdriver.Firefox(service=service, options=options)

    # Timeouts
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)

    print("✅ Firefox driver started successfully")

    # -----------------------------
    # 🌐 OPEN WEBSITE
    # -----------------------------
    url = "https://example.com"
    print(f"Opening: {url}")

    try:
        driver.get(url)
    except TimeoutException:
        print("⚠️ Page load timed out, continuing...")

    # Wait for <body> to be ready
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except:
        print("⚠️ Element wait skipped")

    # -----------------------------
    # 📄 SCRAPE DATA
    # -----------------------------
    print("Page title:", driver.title)

    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"Found {len(links)} links")

    for link in links[:5]:  # print first 5 links
        print(link.text, "->", link.get_attribute("href"))

# -----------------------------
# ❌ ERROR HANDLING
# -----------------------------
except Exception as e:
    print("❌ ERROR:", e)

# -----------------------------
# 🛑 CLEAN EXIT
# -----------------------------
finally:
    try:
        driver.quit()
        print("🛑 Firefox driver closed")
    except:
        pass
    os.system("pkill -f geckodriver")
    os.system("pkill -f firefox")
