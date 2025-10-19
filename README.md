Hello viewers!

This project is a full-stack application consisting of a front end, middleware, and backend. It features a Flask API with light HTML built on top (for demonstration purposes). Users interact with the front end to input their home address, grocery list, and maximum number of stores they’re willing to visit. The application then computes and returns the most cost and distance efficient shopping route. The way this computation is done is by generating possible route combinations using the user’s “max stores” input as the set size, before applying pre-filtering to leave out route combinations that don’t fit the user’s grocery list. Finally, we map out the remaining stores and use a greedy search to find the most optimal (or close to most optimal) route permutation for cost savings. It’s important to note that we use a greedy search in order to greatly speed up computation time compared to A* search and brute force, since the accuracy tradeoff of doing this is very minor. The algorithm also utilizes distance for its cost comparison. For example, the optimizer might recommend a closer, but more expensive, store if the price of gas to travel to a cheaper one outweighs the savings.

Regarding the current state of this project, frontend-to-backend integration isn’t configured just yet, but the intended workflow when pushed to production is as follows:

  Frontend - User will send in their parameters here, and their route will be displayed here. User inputs are sent as a JSON object to the API.
  Flask API - Receives JSON object from the frontend, and then performs computation using data from the backend, before sending its output back to the frontend as a JSON to be displayed.
  Backend Database - A CSV file containing products, prices, the store they belong to, and store location (individual products are aggregated into stores during computation). The CSV will be populated by running a web scraper over retailer websites to get product info.

