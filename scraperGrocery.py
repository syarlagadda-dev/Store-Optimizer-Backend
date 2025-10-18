from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv

# Set up Selenium WebDriver (requires ChromeDriver)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in the background
service = Service(executable_path='/path/to/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

def scrape_dynamic_content(url):
    driver.get(url)
    time.sleep(5)  # Wait for JavaScript to load content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Your scraping logic here
    print(f"Scraped content from dynamic page: {soup.find('h1').text}")

# Define the URL and the refresh interval
target_url = "http://example.com/dynamic-page"
refresh_interval = 60

while True:
    scrape_dynamic_content(target_url)
    time.sleep(refresh_interval)