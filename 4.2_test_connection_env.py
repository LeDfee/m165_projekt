import os
from pymongo import MongoClient

connection_string = os.getenv("MONGODB_URI")

if connection_string is None:
    print("Fehler: Umgebungsvariable MONGODB_URI wurde nicht gefunden.")
    exit()

client = MongoClient(connection_string)

try:
    databases = client.list_database_names()

    print("Verbindung erfolgreich!")
    print("Datenbanken:")

    for database in databases:
        print(f" - {database}")

except Exception as error:
    print("Verbindung fehlgeschlagen.")
    print(error)