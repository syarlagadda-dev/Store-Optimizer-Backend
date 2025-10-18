from bs4 import BeautifulSoup
from bs4 import *
import requests 
import time
import csv



def toAddressTarget(storeName):
    address_dict = {
        "Charlotte East" : "8830 Albemarle Rd, Charlotte, NC",
        "Charlotte Midtown" : "900 Metropolitan Ave, Charlotte, NC",
        "Pineville" : "9531 South Blvd, Charlotte, NC",
    }

    # Prepare for tolerant matching (case-insensitive)
    norm_map = {k.lower(): v for k, v in address_dict.items()}

    if not storeName:
        return "Address not found"

    key = storeName.strip().lower()

    # Exact (case-insensitive) match
    if key in norm_map:
        return norm_map[key]

    # Substring or token-based matching
    key_tokens = [t for t in key.split() if len(t) > 1]
    for k, v in norm_map.items():
        # if mapping key appears inside provided name or vice-versa
        if k in key or key in k:
            return v
        # if all tokens from provided name appear in mapping key
        if key_tokens and all(tok in k for tok in key_tokens):
            return v

    return "Address not found"

def toAddressWalmart(storeName):
    address_dict = {
        "Charlotte" : "7735 N Tryon St, Charlotte, NC",
        "Concord" : "5825 Thunder Rd, Concord, NC 28027",
        "Huntersville" : "11145 Bryton Town Center Dr, Huntersville, NC",
    }

    # Prepare for tolerant matching (case-insensitive)
    norm_map = {k.lower(): v for k, v in address_dict.items()}

    if not storeName:
        return "Address not found"

    key = storeName.strip().lower()

    # Exact (case-insensitive) match
    if key in norm_map:
        return norm_map[key]

    # Substring or token-based matching
    key_tokens = [t for t in key.split() if len(t) > 1]
    for k, v in norm_map.items():
        # if mapping key appears inside provided name or vice-versa
        if k in key or key in k:
            return v
        # if all tokens from provided name appear in mapping key
        if key_tokens and all(tok in k for tok in key_tokens):
            return v

def toAddressHarris(storeName):
    address_dict = {
        "Cochran Commons" : "W Mallard Creek Church Rd CHARLOTTE, NC 28262",
        "Town Center Plaza" : "University City Blvd Charlotte, NC 28213",
        "Highland Creek" : "Highland Shoppes Dr Charlotte, NC 28269",
    }

    # Prepare for tolerant matching (case-insensitive)
    norm_map = {k.lower(): v for k, v in address_dict.items()}

    if not storeName:
        return "Address not found"

    key = storeName.strip().lower()

    # Exact (case-insensitive) match
    if key in norm_map:
        return norm_map[key]

    # Substring or token-based matching
    key_tokens = [t for t in key.split() if len(t) > 1]
    for k, v in norm_map.items():
        # if mapping key appears inside provided name or vice-versa
        if k in key or key in k:
            return v
        # if all tokens from provided name appear in mapping key
        if key_tokens and all(tok in k for tok in key_tokens):
            return v

    return "Address not found"
        #"Trader Joe's, Charlotte" : ,
        #"Sam's Club, " : "Jw Clay Blvd, Charlotte, NC",
        #"BJ's, " : "Lyles Ln. Concord, NC 28027"

def target_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    storeName = "Charlotte"
    address = toAddressHarris(storeName)
    product = soup.find(attrs={'data-test':'product-title'}).text
    price = soup.find(attrs={'data-test':'product-price'}).text
    if "$" in price:
        price = float(product.replace('$',''))
    return(f"Target, {storeName},"+address+","+product+","+price)

def walmart_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    storeName = soup.find(class_="mw-none-m mh2-m truncate tr pl4 ml-auto").text
    address = toAddressWalmart(storeName)
    product = soup.find(attrs={'data-automation-id':'product-title'}).text
    price = soup.find(attrs={'data-automation-id' : 'product-price'}).text
    if "$" in price:
        price = float(product.replace('$',''))
    return(f"Walmart Supercenter,{storeName},"+address+","+product+","+price)

def harris_teeter_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    storeName = soup.find(attrs={'data-testid' : 'CurrentModality-vanityName'}).text
    address = toAddressHarris(storeName)
    product = soup.find(attrs={'data-test-id':'cart-page-item-description'}).text
    price = soup.find(attrs={'data-test-id' : 'product-item-unit-price'}).text
    if "$" in price:
        price = float(product.replace('$',''))
    return(f"Harris Teeter, {storeName},"+address+","+product+","+price)

def aldi_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    storeName = "Aldi"
    address = "10629 Park Rd, Charlotte, NC 28210"
    product = soup.find(class_="product-title").text
    price = soup.find(class_="product-price").text
    if "$" in price:
        price = float(product.replace('$',''))
    return(f"Aldi,,"+product+","+price)

def lidl_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    storeName = "Steele Creek NC"
    address = "S Tryon St Charlotte, NC 28273"
    product = soup.find(class_="product-title").text
    price = soup.find(class_="product-price").text
    if "$" in price:
        price = float(product.replace('$',''))
    return(f"Aldi,,"+product+","+price)

def traderJoes_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    storeName = "Charlotte - North"
    address = "E Arbors Dr Charlotte, NC 28262"
    product = soup.find(class_="product-title").text
    price = soup.find(class_="product-price").text
    if "$" in price:
        price = float(product.replace('$',''))
    return(f"Aldi,,"+product+","+price)

def traderJoes_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    storeName = "Charlotte - North"
    address = "E Arbors Dr Charlotte, NC 28262"
    product = soup.find(class_="product-title").text
    price = soup.find(class_="product-price").text
    if "$" in price:
        price = float(product.replace('$',''))
    return(f"Aldi,,"+product+","+price)

def scrape_dynamic_content(url):
    requests.get(url)
    soup = BeautifulSoup(requests.page_source, 'html.parser')
    print(f"Scraped content from dynamic page: {soup.find('h1').text}")

# Define the URL and the refresh interval
target_url = "https://www.target.com/s?searchTerm=bacon&facetedValue=5zkty&ignoreBrandExactness=true&moveTo=product-list-grid"
walmart_url = "https://www.walmart.com/search?q=bacon&facet=fulfillment_method_in_store%3AIn-store"
aldi_url = "https://www.aldi.us/en/search/?q=bacon"
lidl_url = "https://www.lidl.com/search?query=bacon"
traderjoes_url = "https://www.traderjoes.com/home/search?q=bacon&global=yes"
harris_teeter_url = "https://www.harristeeter.com/search?query=bacon&searchType=default_search&fulfillment=ais"
sams_club_url = "https://www.samsclub.com/s/bacon"
bjs_url = "https://www.bjs.com/search?query=bacon"

refresh_interval = 60

while True:
    scrape_dynamic_content(target_url)
    time.sleep(refresh_interval)