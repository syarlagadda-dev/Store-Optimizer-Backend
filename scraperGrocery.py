from bs4 import BeautifulSoup
import requests 
import time
import csv

def toAddress(storeName):
    address_dict = {
        "Target, Charlotte East" : "8830 Albemarle Rd, Charlotte, NC",
    }
    return address_dict.get(storeName, "Address not found")

def target_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    storeName = soup.find(attrs={'data-test':'store-name'}).text
    address = toAddress(storeName)
    product = soup.find(attrs={'data-test':'product-title'}).text
    if "$" in product:
        product = float(product.replace('$',''))
    price = soup.find(attrs={'data-test':'product-price'}).text
    return(f"Target, {storeName},"+address+","+product+","+price)

def walmart_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    storeName = soup.find(attrs={'data-test':'store-name'}).text
    address = toAddress(storeName)
    product = soup.find(attrs={'data-test':'product-title'}).text
    if "$" in product:
        product = float(product.replace('$',''))
    price = soup.find(attrs={'data-test':'product-price'}).text
    return(f"Target, {storeName},"+address+","+product+","+price)

def scrape_dynamic_content(url):
    requests.get(url)
    soup = BeautifulSoup(requests.page_source, 'html.parser')
    # Your scraping logic here
    print(f"Scraped content from dynamic page: {soup.find('h1').text}")

# Define the URL and the refresh interval
target_url = "https://www.target.com/s?searchTerm=bacon&facetedValue=5zkty&ignoreBrandExactness=true&moveTo=product-list-grid"
walmart_url = "https://www.walmart.com/search/?query=bacon"
aldi_url = "https://www.aldi.us/en/search/?q=bacon"
lidl_url = "https://www.lidl.com/search?query=bacon"
traderjoes_url = "https://www.traderjoes.com/search?query=bacon"
harris_teeter_url = "https://www.harristeeter.com/search?query=bacon"
sams_club_url = "https://www.samsclub.com/s/bacon"
bjs_url = "https://www.bjs.com/search?query=bacon"

refresh_interval = 60

while True:
    scrape_dynamic_content(target_url)
    time.sleep(refresh_interval)