from bs4 import BeautifulSoup
from bs4 import *
import requests 
import time
import csv

def toAddress(storeName):
    address_dict = {
        "Target, Charlotte East" : "8830 Albemarle Rd, Charlotte, NC",
        "Target, Charlotte Midtown" : "900 Metropolitan Ave, Charlotte, NC",
        "Target, Pineville" : "9531 South Blvd, Charlotte, NC",
        "Walmart Supercenter, Charlotte" : "7735 N Tryon St, Charlotte, NC",
        "Walmart Supercenter, Concord" : "5825 Thunder Rd, Concord, NC 28027",
        "Walmart Supercenter, Huntersville" : "11145 Bryton Town Center Dr, Huntersville, NC",
        "Aldi" : "Park Rd., Charlotte, NC 280210",
        "LIDL, Charlotte, NC" : "S Tryon St Charlotte, NC 28273",
        "Trader Joe's, Charlotte" : "E Arbors Dr Charlotte, NC 28262",
        "Harris Teeter, 12190 University City Blvd" : "12190 University City Blvd",
        "Sam's Club, " : "Jw Clay Blvd, Charlotte, NC",
        "BJ's, " : "Lyles Ln. Concord, NC 28027"
    }
    return address_dict.get(storeName, "Address not found")

def target_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    storeName = soup.find(attrs={'data-test':'store-name'}).text
    address = toAddress(storeName)
    product = soup.find(attrs={'data-test':'product-title'}).text
    price = soup.find(attrs={'data-test':'product-price'}).text
    if "$" in price:
        price = float(product.replace('$',''))
    return(f"Target, {storeName},"+address+","+product+","+price)

def walmart_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    storeName = soup.find(class_="mw-none-m mh2-m truncate tr pl4 ml-auto").text
    address = toAddress(storeName)
    product = soup.find(attrs={'data-automation-id':'product-title'}).text
    price = soup.find(attrs={'data-automation-id' : 'product-price'}).text
    if "$" in price:
        price = float(product.replace('$',''))
    return(f"Walmart Supercenter, {storeName},"+address+","+product+","+price)

def harris_teeter_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    storeName = soup.find(attrs={'data-testid' : 'PickupAddressText'}).text
    address = toAddress(storeName)
    product = soup.find(attrs={'data-test-id':'cart-page-item-description'}).text
    price = soup.find(attrs={'data-test-id' : 'product-item-unit-price'}).text
    if "$" in price:
        price = float(product.replace('$',''))
    return(f"Harris Teeter, {storeName},"+address+","+product+","+price)

def aldi_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    storeName = "Aldi"
    address = toAddress(storeName)
    product = soup.find(class_="product-title").text
    price = soup.find(class_="product-price").text
    if "$" in price:
        price = float(product.replace('$',''))
    return(f"Aldi,"+address+","+product+","+price)

def scrape_dynamic_content(url):
    requests.get(url)
    soup = BeautifulSoup(requests.page_source, 'html.parser')
    # Your scraping logic here
    print(f"Scraped content from dynamic page: {soup.find('h1').text}")

# Define the URL and the refresh interval
target_url = "https://www.target.com/s?searchTerm=bacon&facetedValue=5zkty&ignoreBrandExactness=true&moveTo=product-list-grid"
walmart_url = "https://www.walmart.com/search?q=bacon&facet=fulfillment_method_in_store%3AIn-store"
aldi_url = "https://www.aldi.us/en/search/?q=bacon"
lidl_url = "https://www.lidl.com/search?query=bacon"
traderjoes_url = "https://www.traderjoes.com/search?query=bacon"
harris_teeter_url = "https://www.harristeeter.com/search?query=bacon&searchType=default_search&fulfillment=ais"
sams_club_url = "https://www.samsclub.com/s/bacon"
bjs_url = "https://www.bjs.com/search?query=bacon"

refresh_interval = 60

while True:
    scrape_dynamic_content(target_url)
    time.sleep(refresh_interval)