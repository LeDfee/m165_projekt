from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["db_restaurants"]
restaurants = db["restaurants"]

boroughs = restaurants.distinct("borough")

print("Stadtbezirke:")
for borough in boroughs:
    print(f" - {borough}")