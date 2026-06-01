from pymongo import MongoClient
from bson import ObjectId


client = MongoClient("mongodb://localhost:27017")

db = client["room_db"]
rooms_collection = db["rooms"]


class Room:
    def __init__(self, name, size, _id=None):
        self.name = name
        self.size = size
        self.id = _id

    def to_document(self):
        return {
            "name": self.name,
            "size": self.size
        }


class DaoRoom:
    def to_object_id(self, room_id):
        if isinstance(room_id, ObjectId):
            return room_id

        return ObjectId(room_id)

    def insert(self, room):
        result = rooms_collection.insert_one(room.to_document())
        return result.inserted_id

    def get_all(self):
        return list(rooms_collection.find())

    def update(self, room_id, new_name, new_size):
        result = rooms_collection.update_one(
            {"_id": self.to_object_id(room_id)},
            {
                "$set": {
                    "name": new_name,
                    "size": new_size
                }
            }
        )

        return result.modified_count

    def delete(self, room_id):
        result = rooms_collection.delete_one(
            {"_id": self.to_object_id(room_id)}
        )

        return result.deleted_count


def main():
    dao = DaoRoom()

    room = Room("Zimmer 101", 25)
    room_id = dao.insert(room)

    print("Room gespeichert:")
    print(room_id)

    dao.update(room_id, "Zimmer 102", 30)

    print("\nRooms:")
    for room in dao.get_all():
        print(room)

    dao.delete(room_id)
    print("\nTest-Room geloescht.")


if __name__ == "__main__":
    main()
