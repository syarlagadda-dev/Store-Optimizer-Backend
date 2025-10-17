import pandas as pd
import itertools
import math
from geopy.geocoders import Nominatim

# ____________________________   User coordinates will converted to longitude and latitude to help count distance
def get_coords_from_address(address):
    """
    Converts a user address (string) into (lat, lon).
    Returns (None, None) if not found or invalid.
    """
    if not address or address.strip() == "":
        return None, None

    geolocator = Nominatim(user_agent="grocery_optimizer_app")
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"⚠️ Geocoding error: {e}")
        return None, None

# ____________________________   Function to calculate distance between coordinates (in miles)
def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# ____________________________   Main Optimizer (with pre-filtering)
def find_best_combo(csv_path, grocery_list, budget, max_stores, user_address):
    COST_PER_MILE = 0.6

    def all_items_found(chosen_items, grocery_list):
        chosen_names = chosen_items.tolist()
        for g_item in grocery_list:
            if not any(g_item.lower() in c_item.lower() for c_item in chosen_names):
                return False
        return True

    user_lat, user_lon = get_coords_from_address(user_address)
    if user_lat is None or user_lon is None:
        return {"error": "Could not locate your address."}

    # Load data
    data = pd.read_csv(csv_path).dropna(subset=["lat", "lon"])
    if data.empty:
        return {"error": "No stores with valid coordinates available."}

    data["lat"] = data["lat"].astype(float)
    data["lon"] = data["lon"].astype(float)

    # ✅ PRE-FILTER stores that actually sell something from grocery_list
    relevant_data = data[data["item"].str.lower().apply(lambda x: any(g.lower() in x for g in grocery_list))]
    stores = relevant_data["store_name"].unique()

    best_combo = None
    best_total = float("inf")

    # Only iterate over relevant stores
    for r in range(1, max_stores + 1):
        for store_combo in itertools.combinations(stores, r):
            subset = relevant_data[relevant_data["store_name"].isin(store_combo)]
            if subset.empty:
                continue

            chosen = subset.loc[subset.groupby("item")["price"].idxmin()]
            if not all_items_found(chosen["item"], grocery_list):
                continue

            total_price = chosen["price"].sum()

            # ---------------- Greedy nearest-neighbor route ----------------
            store_coords = subset.drop_duplicates("store_name")[["lat", "lon", "address", "store_name"]].values.tolist()
            store_coords = [(float(lat), float(lon), addr, store) for lat, lon, addr, store in store_coords]

            unvisited = store_coords.copy()
            current_lat, current_lon = user_lat, user_lon
            route_distance = 0
            route_order = [{"step": 1, "type": "start", "address": user_address}]
            step_counter = 2

            while unvisited:
                nearest_idx, nearest_store = min(
                    enumerate(unvisited),
                    key=lambda x: haversine(current_lat, current_lon, x[1][0], x[1][1])
                )
                dist_to_nearest = haversine(current_lat, current_lon, nearest_store[0], nearest_store[1])
                route_distance += dist_to_nearest
                current_lat, current_lon = nearest_store[0], nearest_store[1]
                route_order.append({
                    "step": step_counter,
                    "type": "store",
                    "address": f"{nearest_store[3]} - {nearest_store[2]}"
                })
                step_counter += 1
                unvisited.pop(nearest_idx)

            # Return to user
            dist_back = haversine(current_lat, current_lon, user_lat, user_lon)
            route_distance += dist_back
            route_order.append({"step": step_counter, "type": "end", "address": user_address})

            total_with_travel = total_price + route_distance * COST_PER_MILE

            if total_with_travel < best_total and total_with_travel <= budget:
                best_total = total_with_travel
                formatted_items = [
                    f"{row['item']} (${row['price']}) : {row['store_name']} - {row['address']}"
                    for _, row in chosen.iterrows()
                ]
                best_combo = {
                    "stores": list(store_combo),
                    "items": formatted_items,
                    "item_total": float(round(total_price, 2)),
                    "miles_traveled": float(round(route_distance, 2)),
                    "approximate_total_cost": float(round(total_with_travel, 2)),
                    "route_order": route_order
                }

    return best_combo or {"error": "No valid combination found within budget."}

# ___________________ Run example
if __name__ == "__main__":
    print("🛒 Grocery Optimizer Demo 🛒")
    csv_path = "prices_with_coords.csv"  # Make sure this file is in the same folder

    # Sample test run (you can later link this to a frontend)
    user_address = '123 Main St, Charlotte, NC 28202'

    grocery_list = ["milk", "bread", "eggs"]  # You can customize or make this user input
    budget = 40
    max_stores = 3

    result = find_best_combo(csv_path, grocery_list, budget, max_stores, user_address)
    print("\n🔍 Best Shopping Plan:")
    print(result)





# JSON output example
'''
{
  "stores": [
    "Target"
  ],
  "items": [
    "bread ($2.3) : Target - 123 Main St, Charlotte, NC",
    "eggs ($2.9) : Target - 123 Main St, Charlotte, NC",
    "milk ($3.6) : Target - 123 Main St, Charlotte, NC"
  ],
  "item_total": 8.8,
  "miles_traveled": 0.37,
  "approximate_total_cost": 9.02,
  "route_order": [
    {
      "step": 1,
      "type": "start",
      "address": "123 Main St, Charlotte, NC 28202"
    },
    {
      "step": 2,
      "type": "store",
      "address": "Target - 123 Main St, Charlotte, NC"
    },
    {
      "step": 3,
      "type": "end",
      "address": "123 Main St, Charlotte, NC 28202"
    }
  ]
}
'''