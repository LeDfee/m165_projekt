from pymongo import MongoClient
import re

client = MongoClient("mongodb://localhost:27017")

db = client["db_restaurants"]
restaurants = db["restaurants"]

name = input("Name: ").strip()
cuisine = input("Kueche: ").strip()

query = {}

if name != "":
    query["name"] = {
        "$regex": re.escape(name),
        "$options": "i"
    }

if cuisine != "":
    query["cuisine"] = {
        "$regex": re.escape(cuisine),
        "$options": "i"
    }

results = list(restaurants.find(query))

if len(results) == 0:
    print("Keine Restaurants gefunden.")
else:
    print("Gefundene Restaurants:")

    for restaurant in results:
        print(f"{restaurant['name']} | {restaurant['cuisine']} | {restaurant['borough']} | ID: {restaurant['_id']}")
