from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017")

db = client["db_restaurants"]
restaurants = db["restaurants"]


def read_min_length(label, min_length=2):
    while True:
        value = input(f"{label}: ").strip()

        if len(value) >= min_length:
            return value

        print(f"{label} muss mindestens {min_length} Zeichen lang sein.")


def read_zipcode():
    while True:
        value = input("Postleitzahl: ").strip()

        if len(value) == 5:
            return value

        print("Postleitzahl muss genau 5 Zeichen lang sein.")


def main():
    print("Restaurant hinzufuegen")
    print("----------------------")

    name = read_min_length("Name")
    borough = read_min_length("Borough")
    cuisine = read_min_length("Cuisine")
    building = input("Hausnummer: ").strip()
    street = read_min_length("Strasse")
    zipcode = read_zipcode()

    restaurant = {
        "name": name,
        "borough": borough,
        "cuisine": cuisine,
        "address": {
            "building": building,
            "street": street,
            "zipcode": zipcode,
            "coord": []
        },
        "grades": []
    }

    result = restaurants.insert_one(restaurant)

    print("Restaurant wurde gespeichert.")
    print(f"ID: {result.inserted_id}")


if __name__ == "__main__":
    main()
