from pymongo import MongoClient
import re


client = MongoClient("mongodb://localhost:27017")

db = client["db_restaurants"]
restaurants = db["restaurants"]


def read_search_term():
    while True:
        value = input("Name oder Teil des Namens: ").strip()

        if len(value) >= 2:
            return value

        print("Der Suchbegriff muss mindestens 2 Zeichen lang sein.")


def main():
    print("Restaurants loeschen")
    print("--------------------")

    search_term = read_search_term()

    query = {
        "name": {
            "$regex": re.escape(search_term),
            "$options": "i"
        }
    }

    found = list(restaurants.find(query, {"name": 1, "borough": 1, "cuisine": 1}))

    if len(found) == 0:
        print("Keine Restaurants gefunden.")
        return

    print(f"{len(found)} Restaurant(s) gefunden:")

    for restaurant in found:
        print(
            f" - {restaurant.get('name')} | "
            f"{restaurant.get('cuisine')} | "
            f"{restaurant.get('borough')} | "
            f"ID: {restaurant.get('_id')}"
        )

    answer = input("Sollen diese Restaurants geloescht werden? (ja/nein): ")
    answer = answer.strip().lower()

    if answer != "ja":
        print("Es wurde nichts geloescht.")
        return

    result = restaurants.delete_many(query)
    print(f"{result.deleted_count} Restaurant(s) wurden geloescht.")


if __name__ == "__main__":
    main()
