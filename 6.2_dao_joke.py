from pymongo import MongoClient
from bson import ObjectId


client = MongoClient("mongodb://localhost:27017")

db = client["jokes_db"]
jokes_collection = db["jokes"]


class Joke:
    def __init__(self, text, category, author, _id=None):
        self.text = text
        self.category = category
        self.author = author
        self.id = _id

    def to_document(self):
        return {
            "text": self.text,
            "category": self.category,
            "author": self.author
        }


class DaoJoke:
    def to_object_id(self, joke_id):
        if isinstance(joke_id, ObjectId):
            return joke_id

        return ObjectId(joke_id)

    def insert(self, joke):
        result = jokes_collection.insert_one(joke.to_document())
        return result.inserted_id

    def get_category(self, category):
        return list(
            jokes_collection.find({
                "category": category
            })
        )

    def delete(self, joke_id):
        result = jokes_collection.delete_one(
            {"_id": self.to_object_id(joke_id)}
        )

        return result.deleted_count


def main():
    dao = DaoJoke()

    joke = Joke(
        text="Why do programmers prefer dark mode? Because light attracts bugs.",
        category=["Programming", "IT"],
        author="Dmytro"
    )

    joke_id = dao.insert(joke)

    print("Joke gespeichert:")
    print(joke_id)

    print("\nJokes in Kategorie Programming:")

    jokes = dao.get_category("Programming")

    for joke in jokes:
        print(joke)

    dao.delete(joke_id)
    print("\nTest-Joke geloescht.")


if __name__ == "__main__":
    main()
