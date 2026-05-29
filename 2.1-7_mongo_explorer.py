from pymongo import MongoClient
from bson import ObjectId
import os


client = MongoClient("mongodb://localhost:27017")


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def wait_and_restart():
    input("\nPress any button to return")


def print_list(title, items):
    print(title)

    if not items:
        print(f"No {title[:-1]}")
        wait_and_restart()
        return False

    for item in items:
        print(f" - {item}")

    return True


def select_from_list(prompt, items, element_name):
    while True:
        selected = input(f"\n{prompt}: ").strip()

        if selected in items:
            return selected

        print(f"{element_name} does not exist. Please try again.")


def show_document_content(db_name, collection_name, document_id):
    clear_console()

    db = client[db_name]
    collection = db[collection_name]

    document = collection.find_one({"_id": ObjectId(document_id)})

    print(f"{db_name}.{collection_name}.{document_id}\n")

    if document is None:
        print("No Document")
        wait_and_restart()
        return

    for key, value in document.items():
        print(f"{key}: {value}")

    wait_and_restart()


def select_document(db_name, collection_name):
    clear_console()

    db = client[db_name]
    collection = db[collection_name]

    documents = list(collection.find({}, {"_id": 1}))
    document_ids = [str(doc["_id"]) for doc in documents]

    print(f"{db_name}.{collection_name}\n")

    if not print_list("Documents", document_ids):
        return

    while True:
        selected_id = input("\nSelect Document: ").strip()

        if selected_id in document_ids:
            show_document_content(db_name, collection_name, selected_id)
            return

        print("Document does not exist. Please try again.")


def select_collection(db_name):
    clear_console()

    db = client[db_name]
    collections = db.list_collection_names()

    print(f"{db_name}\n")

    if not print_list("Collections", collections):
        return

    collection_name = select_from_list(
        "Select Collection",
        collections,
        "Collection"
    )

    select_document(db_name, collection_name)


def select_database():
    clear_console()

    databases = client.list_database_names()

    print("Databases")

    if not databases:
        print("No Database")
        wait_and_restart()
        return

    for db in databases:
        print(f" - {db}")

    db_name = select_from_list(
        "Select Database",
        databases,
        "Database"
    )

    select_collection(db_name)


def main():
    while True:
        select_database()


if __name__ == "__main__":
    main()