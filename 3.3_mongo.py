from pymongo import MongoClient
import math

client = MongoClient("mongodb://localhost:27017")

db = client["db_restaurants"]
restaurants = db["restaurants"]


def calculate_distance(coord1, coord2):
    lon1, lat1 = coord1
    lon2, lat2 = coord2

    return math.sqrt((lon1 - lon2) ** 2 + (lat1 - lat2) ** 2)


def has_valid_coord(restaurant):
    coord = restaurant.get("address", {}).get("coord")
    return isinstance(coord, list) and len(coord) == 2


le_perigord = restaurants.find_one({"name": "Le Perigord"})

if le_perigord is None:
    print("Le Perigord wurde nicht gefunden.")
elif not has_valid_coord(le_perigord):
    print("Le Perigord hat keine gueltigen Koordinaten.")
else:
    le_perigord_coord = le_perigord["address"]["coord"]

    nearest_restaurant = None
    nearest_distance = None

    for restaurant in restaurants.find({
        "name": {"$ne": "Le Perigord"},
        "address.coord": {"$exists": True}
    }):
        if not has_valid_coord(restaurant):
            continue

        coord = restaurant["address"]["coord"]
        distance = calculate_distance(le_perigord_coord, coord)

        if nearest_distance is None or distance < nearest_distance:
            nearest_distance = distance
            nearest_restaurant = restaurant

    if nearest_restaurant is None:
        print("Kein anderes Restaurant mit Koordinaten gefunden.")
    else:
        print("Naechstes Restaurant:")
        print(f"Name: {nearest_restaurant['name']}")
        print(f"Kueche: {nearest_restaurant['cuisine']}")
        print(f"Bezirk: {nearest_restaurant['borough']}")
        print(f"Adresse: {nearest_restaurant['address']}")
