from pymongo import MongoClient
from datetime import datetime
import re

client = MongoClient("mongodb://localhost:27017")

db = client["db_restaurants"]
restaurants = db["restaurants"]


def search_restaurants():
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
        return []

    print("\nGefundene Restaurants:")

    for index, restaurant in enumerate(results, start=1):
        print(
            f"{index}. {restaurant['name']} | "
            f"{restaurant['cuisine']} | "
            f"{restaurant['borough']} | "
            f"ID: {restaurant['_id']}"
        )

    return results


def select_restaurant(results):
    if len(results) == 1:
        selected = results[0]
        print(f"\nAusgewaehltes Restaurant: {selected['name']}")
        return selected["_id"]

    while True:
        choice = input("\nWaehle ein Restaurant mit Nummer: ").strip()

        if not choice.isdigit():
            print("Bitte eine gueltige Zahl eingeben.")
            continue

        choice = int(choice)

        if 1 <= choice <= len(results):
            selected = results[choice - 1]
            print(f"\nAusgewaehltes Restaurant: {selected['name']}")
            return selected["_id"]

        print("Diese Nummer existiert nicht.")


def add_rating(restaurant_id):
    while True:
        score_input = input("Bewertung / Score eingeben: ").strip()

        if score_input.lstrip("-").isdigit():
            score = int(score_input)
            break

        print("Bitte eine Zahl eingeben.")

    new_grade = {
        "date": datetime.now(),
        "grade": "User",
        "score": score
    }

    restaurants.update_one(
        {"_id": restaurant_id},
        {
            "$push": {
                "grades": new_grade
            }
        }
    )

    print("Bewertung wurde gespeichert.")


def main():
    while True:
        print("\nRestaurant-Suche")
        print("----------------")

        results = search_restaurants()

        if len(results) > 0:
            restaurant_id = select_restaurant(results)

            answer = input("\nMoechtest du eine Bewertung hinzufuegen? (ja/nein): ").strip().lower()

            if answer == "ja":
                add_rating(restaurant_id)

        again = input("\nNeue Suche? (ja/nein): ").strip().lower()

        if again != "ja":
            break


if __name__ == "__main__":
    main()
