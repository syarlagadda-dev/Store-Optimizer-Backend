from bs4 import BeautifulSoup
import requests
import time
import csv
import lxml

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- Fast HTTP session with pooling/retries ---
SESSION = requests.Session()
_retry = Retry(
    total=3, backoff_factor=0.5,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=frozenset(["GET", "HEAD"]),
)
_adapter = HTTPAdapter(pool_connections=50, pool_maxsize=50, max_retries=_retry)
SESSION.mount("http://", _adapter)
SESSION.mount("https://", _adapter)
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})
REQUEST_TIMEOUT = (3.05, 12)  # (connect, read)

def fetch(url, **kwargs):
    """Wrapper around SESSION.get with sane default timeout."""
    if "timeout" not in kwargs:
        kwargs["timeout"] = REQUEST_TIMEOUT
    return SESSION.get(url, **kwargs)

# --- In-memory row collector (thread-safe) ---
_ROWS_LOCK = threading.Lock()
_ROWS = []

def _append_row_to_csv(row):
    """Collect rows in memory (thread-safe) and write once at the end."""
    with _ROWS_LOCK:
        _ROWS.append(tuple(row))

def _write_csv_once(csv_path):
    # dedupe while preserving order
    unique = list(dict.fromkeys(_ROWS))
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerows(unique)
    return len(unique)

CSV_PATH = "prices_with_coords.csv"

# --- ADDRESS MAPPING DATA (Defined Once Globally for efficiency) ---
TARGET_ADDRESSES = {
    "Charlotte East" : "8830 Albemarle Rd, Charlotte, NC",
    "Charlotte Midtown" : "900 Metropolitan Ave, Charlotte, NC",
    "Pineville" : "9531 South Blvd, Charlotte, NC",
}
WALMART_ADDRESSES = {
    "Charlotte" : "7735 N Tryon St, Charlotte, NC",
    "Concord" : "5825 Thunder Rd, Concord, NC 28027",
    "Huntersville" : "11145 Bryton Town Center Dr, Huntersville, NC",
}
HARRIS_ADDRESSES = {
    "Cochran Commons" : "W Mallard Creek Church Rd CHARLOTTE, NC 28262",
    "Town Center Plaza" : "University City Blvd Charlotte, NC 28213",
    "Highland Creek" : "Highland Shoppes Dr Charlotte, NC 28269",
}

# --- Utility and Mapping Functions (Unchanged for correctness/efficiency) ---

def _append_row_to_csv(store_name_full, store_name_loc, address, item, price_value, csv_path=CSV_PATH):
    """Append a row to CSV."""
    header = ["store_name", "store_location", "address", "item", "price", "lat", "lon"]
    write_header = True
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            if f.read().strip():
                write_header = False
    except FileNotFoundError:
        write_header = True

    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow([store_name_full, store_name_loc, address, item, price_value, "", ""])


def _tolerant_address_map(storeName, address_dict):
    """Generic function for tolerant address matching."""
    norm_map = {k.lower(): v for k, v in address_dict.items()}

    if not storeName:
        return "Address not found"

    key = storeName.strip().lower()
    if key in norm_map:
        return norm_map[key]

    key_tokens = [t for t in key.split() if len(t) > 1]
    for k, v in norm_map.items():
        if k in key or key in k:
            return v
        if key_tokens and all(tok in k for tok in key_tokens):
            return v
    return "Address not found"

def toAddressTarget(storeName):
    return _tolerant_address_map(storeName, TARGET_ADDRESSES)

def toAddressWalmart(storeName):
    return _tolerant_address_map(storeName, WALMART_ADDRESSES)

def toAddressHarris(storeName):
    return _tolerant_address_map(storeName, HARRIS_ADDRESSES)

# --- Scraper functions (Logic kept from corrected version) ---
# NOTE: The *actual* time taken depends on network speed and website response time.
# If all sites load quickly, the run time will be under 60 seconds.

def target_scraper(url):
    response = fetch(url)
    soup = BeautifulSoup(response.text, "lxml")
    storeName_loc = "Charlotte"
    address = toAddressTarget(storeName_loc)
    product = soup.find(attrs={'data-test':'product-title'})
    price = soup.find(attrs={'data-test':'product-price'})
    product_text = product.text.strip() if product else "Product Title Not Found"
    price_text = price.text.strip() if price else "Price Not Found"
    if "$" in price_text:
        price_value = float(price_text.replace('$','').replace('each','').strip())
    else:
        price_value = price_text
    _append_row_to_csv("Target", storeName_loc, address, product_text, price_value)

def walmart_scraper(url):
    response = fetch(url)
    soup = BeautifulSoup(response.text, "lxml")
    storeName_el = soup.find(class_="mw-none-m mh2-m truncate tr pl4 ml-auto")
    product_el = soup.find(attrs={'data-automation-id':'product-title'})
    price_el = soup.find(attrs={'data-automation-id' : 'product-price'})
    storeName_loc = storeName_el.text.strip() if storeName_el else "Store Loc Not Found"
    product_text = product_el.text.strip() if product_el else "Product Title Not Found"
    price_text = price_el.text.strip() if price_el else "Price Not Found"
    address = toAddressWalmart(storeName_loc)
    if "$" in price_text:
        price_value = float(price_text.replace('$','').strip())
    else:
        price_value = price_text
    _append_row_to_csv("Walmart Supercenter", storeName_loc, address, product_text, price_value)

def harris_teeter_scraper(url):
    response = fetch(url)
    soup = BeautifulSoup(response.text, "lxml")
    storeName_el = soup.find(attrs={'data-testid' : 'CurrentModality-vanityName'})
    product_el = soup.find(attrs={'data-test-id':'cart-page-item-description'})
    price_el = soup.find(attrs={'data-test-id' : 'product-item-unit-price'})
    storeName_loc = storeName_el.text.strip() if storeName_el else "Store Loc Not Found"
    product_text = product_el.text.strip() if product_el else "Product Title Not Found"
    price_text = price_el.text.strip() if price_el else "Price Not Found"
    address = toAddressHarris(storeName_loc)
    if "$" in price_text:
        price_value = float(price_text.replace('$','').strip())
    else:
        price_value = price_text
    _append_row_to_csv("Harris Teeter", storeName_loc, address, product_text, price_value)

def aldi_scraper(url):
    response = fetch(url)
    soup = BeautifulSoup(response.text, "lxml")
    storeName_loc = "Aldi - Park Rd"
    address = "10629 Park Rd, Charlotte, NC 28210"
    product_el = soup.find(class_="product-title")
    price_el = soup.find(class_="product-price")
    product_text = product_el.text.strip() if product_el else "Product Title Not Found"
    price_text = price_el.text.strip() if price_el else "Price Not Found"
    if "$" in price_text:
        price_value = float(price_text.replace('$','').strip())
    else:
        price_value = price_text
    _append_row_to_csv("Aldi", storeName_loc, address, product_text, price_value)

def lidl_scraper(url):
    response = fetch(url)
    soup = BeautifulSoup(response.text, "lxml")
    storeName_loc = "Steele Creek NC"
    address = "S Tryon St Charlotte, NC 28273"
    product_el = soup.find(class_="_title_1qtbv_71")
    price_el = soup.find(class_="_price_yvlk6_35")
    product_text = product_el.text.strip() if product_el else "Product Title Not Found"
    price_text = price_el.text.strip() if price_el else "Price Not Found"
    if "$" in price_text:
        price_value = float(price_text.replace('$','').replace('*','').strip())
    else:
        price_value = price_text
    _append_row_to_csv("LIDL", storeName_loc, address, product_text, price_value)

def traderJoes_scraper(url):
    response = fetch(url)
    soup = BeautifulSoup(response.text, "lxml")
    storeName_loc = "Charlotte - North"
    address = "E Arbors Dr Charlotte, NC 28262"
    product_el = soup.find(class_="Link_link__1AZfr SearchResultCard_searchResultCard__titleLink__2nz6x")
    price_el = soup.find(class_="ProductPrice_productPrice__price__3-50j")
    product_text = product_el.text.strip() if product_el else "Product Title Not Found"
    price_text = price_el.text.strip() if price_el else "Price Not Found"
    if "$" in price_text:
        price_value = float(price_text.replace('$','').strip())
    else:
        price_value = price_text
    _append_row_to_csv("Trader Joe's", storeName_loc, address, product_text, price_value)

def sams_club_scraper(url):
    response = fetch(url)
    soup = BeautifulSoup(response.text, "lxml")
    storeName_loc = "Charlotte Sam's Club #6540"
    address = "Jw Clay Blvd, Charlotte, NC"
    product_el = soup.find(attrs={'data-automation-id':'product-title'})
    price_el = soup.find(attrs={'data-automation-id' : 'product-price'})
    product_text = product_el.text.strip() if product_el else "Product Title Not Found"
    price_text = price_el.text.strip() if price_el else "Price Not Found"
    if "$" in price_text:
        price_value = float(price_text.replace('$','').strip())
    else:
        price_value = price_text
    _append_row_to_csv("Sam's Club", storeName_loc, address, product_text, price_value)

def bjs_scraper(url):
    response = fetch(url)
    soup = BeautifulSoup(response.text, "lxml")
    storeName_loc = "Concord, NC"
    address = "Lyles Ln. Concord, NC 28027"
    product_el = soup.find(class_="ProductTitlestyle__ProductTitleStyle-sc-1ypnhsh-0 juKbdo")
    price_el = soup.find(class_="Textstyle__StyledText-sc-1lq8adg-0 eYHhHv display-price ")
    product_text = product_el.text.strip() if product_el else "Product Title Not Found"
    price_text = price_el.text.strip() if price_el else "Price Not Found"
    if "$" in price_text:
        price_value = float(price_text.replace('$','').strip())
    else:
        price_value = price_text
    _append_row_to_csv("BJ's", storeName_loc, address, product_text, price_value)


# --- EXECUTION ---
target_url = "https://www.target.com/s?searchTerm=bacon&facetedValue=5zkty&ignoreBrandExactness=true&moveTo=product-list-grid"
walmart_url = "https://www.walmart.com/search?q=bacon&facet=fulfillment_method_in_store%3AIn-store"
aldi_url = "https://www.aldi.us/en/search/?q=bacon"
lidl_url = "https://www.lidl.com/search?query=bacon"
traderjoes_url = "https://www.traderjoes.com/home/search?q=bacon&global=yes"
harris_teeter_url = "https://www.harristeeter.com/search?query=bacon&searchType=default_search&fulfillment=ais"
sams_club_url = "https://www.samsclub.com/s/bacon"
bjs_url = "https://www.bjs.com/search?query=bacon"



def run_parallel_scrape(max_workers=8):
    """Run all *_scraper functions in parallel and write CSV once."""
    t_start = time.perf_counter()
    # Build tasks by pairing *_scraper with *_url
    funcs = {name: obj for name, obj in globals().items() if callable(obj) and name.endswith("_scraper")}
    urls = {name: val for name, val in globals().items() if isinstance(val, str) and name.endswith("_url")}
    tasks = []

    def pick_url_for(fname):
        key = fname.replace("_scraper", "")
        candidates = [
            f"{key}_url",
            f"{key.lower()}_url",
            f"{key.replace('_','')}_url",
            f"{key.replace('_','').lower()}_url",
        ]
        if "trader" in key.lower():
            candidates += ["traderjoes_url", "traderJoes_url"]
        for c in candidates:
            if c in urls:
                return urls[c]
        return None

    for fname, func in funcs.items():
        url = pick_url_for(fname)
        if url:
            tasks.append((fname, func, url))

    if not tasks:
        print("No scraper tasks found.")
        return

    print(f"Running {len(tasks)} scrapers with {max_workers} threads...")
    timings = {}
    errors = 0
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        fut2name = {}
        for fname, func, url in tasks:
            t0 = time.perf_counter()
            fut = ex.submit(func, url)
            fut2name[fut] = (fname, t0)
        for fut in as_completed(fut2name):
            fname, t0 = fut2name[fut]
            try:
                fut.result()
                dt = time.perf_counter() - t0
                timings[fname] = dt
                print(f"✔ {fname} finished in {dt:.2f}s")
            except Exception as e:
                errors += 1
                dt = time.perf_counter() - t0
                timings[fname] = dt
                print(f"✖ {fname} failed in {dt:.2f}s: {e}")

    n = _write_csv_once(CSV_PATH)
    total = time.perf_counter() - t_start
    print(f"\nWrote {n} rows to {CSV_PATH}")
    print("Per-store timings (s):", {k: round(v, 2) for k, v in timings.items()})
    print(f"Total elapsed: {total:.2f}s")
    if total < 60:
        print("✅ Under 60 seconds!")
    else:
        print("⚠ Took over 60 seconds; tighten timeouts, reduce parsing, or increase max_workers.")


def run_single_scrape():
    """Executes all scraping functions once."""
    print(f"--- Scraping cycle started at {time.ctime()} ---")
    
    # Run all scrapers
    harris_teeter_scraper(harris_teeter_url)
    target_scraper(target_url) 
    walmart_scraper(walmart_url)
    aldi_scraper(aldi_url)
    lidl_scraper(lidl_url)
    traderJoes_scraper(traderjoes_url)
    sams_club_scraper(sams_club_url)
    bjs_scraper(bjs_url)
    
    print("--- Scraping cycle finished. Data written to CSV. ---")


if __name__ == "__main__":
    start_time = time.time()
    run_parallel_scrape(max_workers=8)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Total execution time: {duration:.2f} seconds.")
    if duration < 60:
        print("Success: Program wrote to CSV in less than 60 seconds.")
    else:
        print("Warning: Program took longer than 60 seconds. Consider increasing max_workers or tightening timeouts.")