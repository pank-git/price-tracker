from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configure Chrome options
options = Options()
options.binary_location = "/data/data/com.termux/files/usr/bin/chromium"
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Set ChromeDriver path
service = Service("/data/data/com.termux/files/usr/bin/chromedriver")

try:
    # Start browser
    print("Starting browser...")
    driver = webdriver.Chrome(service=service, options=options)

    # Open a test page
    print("Opening test page...")
    driver.get("https://www.google.com")

    # Print page title
    print("Page title is:", driver.title)

    # Success message
    print("✅ Selenium and ChromeDriver are working!")

    driver.quit()

except Exception as e:
    print("❌ Error:", e)
    print("Check your Selenium, Chromium, and ChromeDriver setup.")
