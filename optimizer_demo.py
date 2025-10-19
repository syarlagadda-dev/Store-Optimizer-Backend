from flask import Flask, request, render_template_string
from flask_cors import CORS
import pandas as pd
import itertools
import math
from geopy.geocoders import Nominatim

app = Flask(__name__)
CORS(app)

# ----------------- Helper Functions -----------------
def get_coords_from_address(address):
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


def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# ----------------- Main Optimizer -----------------
def find_best_combo(csv_path, grocery_list, max_stores, user_address):
    COST_PER_MILE = 0.6

    def all_items_found(chosen_items, grocery_list):
        chosen_names = chosen_items.tolist()
        for g_item in grocery_list:
            if not any(g_item.lower() in c_item.lower() for c_item in chosen_names):
                return False
        return True

    error_status = False
    error_message = "error: "

    user_lat, user_lon = get_coords_from_address(user_address)
    if user_lat is None or user_lon is None:
        error_status = True
        error_message += "Could not locate your address. "
    if grocery_list is None:
        error_status = True
        error_message += "No item list. "
    if max_stores is None:
        error_status = True
        error_message += "Please indicate maximum stores. "

    if error_status:
        return {"error": error_message.strip()}

    # Load data
    data = pd.read_csv(csv_path).dropna(subset=["lat", "lon"])
    if data.empty:
        return {"error": "No stores with valid coordinates available."}

    data["lat"] = data["lat"].astype(float)
    data["lon"] = data["lon"].astype(float)

    relevant_data = data[data["item"].str.lower().apply(lambda x: any(g.lower() in x for g in grocery_list))]
    stores = relevant_data["store_name"].unique()

    best_combo = None
    best_total = float("inf")

    for r in range(1, max_stores + 1):
        for store_combo in itertools.combinations(stores, r):
            subset = relevant_data[relevant_data["store_name"].isin(store_combo)]
            if subset.empty:
                continue

            chosen = subset.loc[subset.groupby("item")["price"].idxmin()]
            if not all_items_found(chosen["item"], grocery_list):
                continue

            total_price = chosen["price"].sum()  # grocery-only cost

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

            dist_back = haversine(current_lat, current_lon, user_lat, user_lon)
            route_distance += dist_back
            route_order.append({"step": step_counter, "type": "end", "address": user_address})

            total_with_travel = total_price + route_distance * COST_PER_MILE

            if total_with_travel < best_total:
                best_total = total_with_travel
                formatted_items = [
                    f"{row['item']} (${row['price']}) : {row['store_name']} - {row['address']}"
                    for _, row in chosen.iterrows()
                ]
                best_combo = {
                    "stores": list(store_combo),
                    "items": formatted_items,
                    "grocery_cost": float(round(total_price, 2)),
                    "miles_traveled": float(round(route_distance, 2)),
                    "travel_cost": float(round(route_distance * COST_PER_MILE, 2)),
                    "approximate_total_cost": float(round(total_with_travel, 2)),
                    "route_order": route_order
                }

    return best_combo or {"error": "No valid combination found. Try changing your max stores or item list."}


# ----------------- Web Route -----------------
@app.route("/", methods=["GET", "POST"])
def home():
    result_html = ""
    error_message = ""
    
    if request.method == "POST":
        csv_path = "prices_with_coords.csv"  # static path
        grocery_list = request.form.get("grocery_list", "").split(",")
        max_stores = int(request.form.get("max_stores", 3))
        user_address = request.form.get("home_address", "")
        
        optimizer_result = find_best_combo(csv_path, grocery_list, max_stores, user_address)
        
        if "error" in optimizer_result:
            error_message = f"<p style='color:red'>{optimizer_result['error']}</p>"
        else:
            result_html += "<h2>🛍 Items</h2><ul>"
            for item in optimizer_result["items"]:
                result_html += f"<li>{item}</li>"
            result_html += "</ul>"

            result_html += f"<p><strong>🛒 Grocery Cost:</strong> ${optimizer_result['grocery_cost']}</p>"
            result_html += f"<p><strong>🚗 Travel Cost:</strong> ${optimizer_result['travel_cost']}</p>"
            result_html += f"<p><strong>💰 Total Cost:</strong> ${optimizer_result['approximate_total_cost']}</p>"
            result_html += f"<p><strong>Distance Traveled:</strong> {optimizer_result['miles_traveled']} miles</p>"

            result_html += "<h2>🗺 Route</h2><ol>"
            for step in optimizer_result["route_order"]:
                result_html += f"<li>{step['type'].capitalize()}: {step['address']}</li>"
            result_html += "</ol>"

            result_html += "<h2>🏬 Stores to Visit</h2><ul>"
            for store in optimizer_result["stores"]:
                result_html += f"<li>{store}</li>"
            result_html += "</ul>"

    html = f"""
    <html>
    <head>
      <title>Grocery Optimizer</title>
    </head>
    <body>
      <h1>🛒 Grocery Optimizer</h1>
      {error_message}
      <form method="POST">
        <label>Starting Address:</label><br>
        <input type="text" name="home_address" placeholder="123 Main St, Charlotte, NC" required style="width:400px"><br><br>

        <label>Grocery List (comma separated, no spaces):</label><br>
        <input type="text" name="grocery_list" placeholder="bread,milk,eggs" required style="width:400px"><br><br>

        <label>Max Number of Stores:</label><br>
        <input type="number" name="max_stores" min="1" max="10" value="3"><br><br>

        <input type="submit" value="Optimize Route">
      </form>
      <hr>
      {result_html}
    </body>
    </html>
    """
    return render_template_string(html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)




# CONNECTION DIRECTIONS :) !!!
   # *Note, must have all python libraries pip installed for this to work

# Step 1:
            # Open up powershell, and change directory to the Store-Optimizer-Backend repository in your file system: 
            # ex. cd "C:\Users\susha\OneDrive\Documents\GitHub Repositories\Store-Optimizer-Backend"


# Step 2:
            # Input command: python optimizer_demo.py
            # open a new page in your browser, and put in the page url: http://127.0.0.1:5000/


# You're in!