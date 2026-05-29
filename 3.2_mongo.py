from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["db_restaurants"]
restaurants = db["restaurants"]

pipeline = [
    {
        "$project": {
            "name": 1,
            "borough": 1,
            "cuisine": 1,
            "averageScore": {
                "$avg": "$grades.score"
            }
        }
    },
    {
        "$sort": {
            "averageScore": -1
        }
    },
    {
        "$limit": 3
    }
]

results = restaurants.aggregate(pipeline)

print("Top 3 Restaurants:")
for restaurant in results:
    print(f"{restaurant['name']} | {restaurant['cuisine']} | Durchschnitt: {restaurant['averageScore']}")