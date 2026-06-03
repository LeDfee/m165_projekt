from pymongo import MongoClient
import gridfs
import os

client = MongoClient("mongodb://localhost:27017")

db = client["photo_album"]
fs = gridfs.GridFS(db)


def add_photo():
    album = input("Album: ").strip()
    path = input("Bild-Pfad: ").strip()

    if album == "":
        print("Album darf nicht leer sein.")
        return

    if not os.path.exists(path):
        print("Datei wurde nicht gefunden.")
        return

    with open(path, "rb") as file:
        file_id = fs.put(
            file,
            filename=os.path.basename(path),
            metadata={
                "album": album
            }
        )

    print("Foto gespeichert.")
    print(f"File ID: {file_id}")


def download_album():
    album = input("Album: ").strip()
    target_folder = input("Zielordner: ").strip()

    if target_folder == "":
        target_folder = "."

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    files = db.fs.files.find({
        "metadata.album": album
    })

    count = 0

    for file_info in files:
        file_id = file_info["_id"]
        filename = file_info["filename"]

        stored_file = fs.get(file_id)

        target_path = os.path.join(target_folder, filename)

        with open(target_path, "wb") as output:
            output.write(stored_file.read())

        print(f"Heruntergeladen: {target_path}")
        count += 1

    if count == 0:
        print("Keine Fotos in diesem Album gefunden.")
    else:
        print(f"{count} Foto(s) heruntergeladen.")


def show_albums():
    albums = db.fs.files.distinct("metadata.album")

    if len(albums) == 0:
        print("Keine Alben vorhanden.")
        return

    print("Alben:")

    for album in albums:
        print(f" - {album}")


def main():
    while True:
        print("\nFotoalbum")
        print("---------")
        print("1. Foto hinzufuegen")
        print("2. Fotos eines Albums herunterladen")
        print("3. Alben anzeigen")
        print("4. Beenden")

        choice = input("Auswahl: ").strip()

        if choice == "1":
            add_photo()
        elif choice == "2":
            download_album()
        elif choice == "3":
            show_albums()
        elif choice == "4":
            break
        else:
            print("Ungueltige Auswahl.")


if __name__ == "__main__":
    main()
