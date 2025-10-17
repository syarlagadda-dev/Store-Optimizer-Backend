from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from geocode_stores import update_geocodes
from optimizer import find_best_combo  # Your existing optimizer

app = Flask(__name__)

# ---------- Background job setup ----------
scheduler = BackgroundScheduler()
scheduler.add_job(update_geocodes, 'interval', hours=1)  # run every hour
scheduler.start()

# ---------- Routes ----------
@app.route('/')
def home():
    return "🛒 Grocery Optimizer API is running!"

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.json
    grocery_list = data['items']
    budget = float(data['budget'])
    max_stores = int(data['max_stores'])
    user_address = data['address']

    result = find_best_combo(
        csv_path='prices_with_coords.csv',
        grocery_list=grocery_list,
        budget=budget,
        max_stores=max_stores,
        user_address=user_address
    )

    return jsonify(result)

# Optional: trigger geocoding manually
@app.route('/update_geocodes', methods=['POST'])
def manual_geocode():
    update_geocodes()
    return jsonify({"status": "Geocoding run completed."})

if __name__ == '__main__':
    app.run(debug=True)