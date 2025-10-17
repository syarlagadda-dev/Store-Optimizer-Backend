import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep

CSV_PATH = "prices_with_coords.csv"

def update_geocodes():
    """
    Fills empty latitude/longitude for each row in the CSV without overwriting
    store_name or address. Adds retries and longer timeout for reliability.
    """
    geolocator = Nominatim(user_agent="grocery_optimizer_app")
    data = pd.read_csv(CSV_PATH)

    # Ensure lat/lon columns exist
    if "lat" not in data.columns:
        data["lat"] = None
    if "lon" not in data.columns:
        data["lon"] = None

    cache = {}
    MAX_RETRIES = 3

    for i, row in data.iterrows():
        # Only fill missing lat/lon
        if pd.notnull(row["lat"]) and pd.notnull(row["lon"]):
            continue

        store_name = row["store_name"]
        address = row["address"]

        # Skip empty addresses
        if not isinstance(address, str) or address.strip() == "":
            print(f"⚠️ Skipping empty address at row {i}")
            continue

        # Check cache
        if address in cache:
            lat, lon = cache[address]
        else:
            lat, lon = None, None
            # Retry loop
            for attempt in range(MAX_RETRIES):
                try:
                    # Include store name in query for better geocoding
                    query = f"{store_name}, {address}"
                    location = geolocator.geocode(query, timeout=10)
                    if location:
                        lat, lon = location.latitude, location.longitude
                        print(f"✅ Geocoded: {store_name}")
                        break
                except Exception as e:
                    print(f"⚠️ Retry {attempt+1} failed for {store_name}: {e}")
                    sleep(1)  # Wait before retrying

            if lat is None or lon is None:
                print(f"❌ Could not geocode: {store_name}")

            cache[address] = (lat, lon)
            sleep(1)  # Respect Nominatim rate limits

        # Fill only empty lat/lon
        if pd.isnull(row["lat"]):
            data.at[i, "lat"] = lat
        if pd.isnull(row["lon"]):
            data.at[i, "lon"] = lon

    data.to_csv(CSV_PATH, index=False)
    print("✅ CSV updated with latitude and longitude.")

# Local run
if __name__ == "__main__":
    update_geocodes()