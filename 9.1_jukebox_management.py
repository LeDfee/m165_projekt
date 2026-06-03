from pymongo import MongoClient
import gridfs
import os
import re


client = MongoClient("mongodb://localhost:27017")

db = client["jukebox"]
fs = gridfs.GridFS(db)


class Song:
    def __init__(self, name, artist, album="", genre="", year=""):
        self.name = name
        self.artist = artist
        self.album = album
        self.genre = genre
        self.year = year

    def to_metadata(self):
        return {
            "type": "song",
            "name": self.name,
            "artist": self.artist,
            "album": self.album,
            "genre": self.genre,
            "year": self.year
        }


def read_required(label):
    while True:
        value = input(f"{label}: ").strip()

        if value != "":
            return value

        print(f"{label} ist ein Pflichtfeld.")


def read_optional(label):
    return input(f"{label}: ").strip()


def build_search_query():
    name = input("Name suchen: ").strip()
    artist = input("Interpret suchen: ").strip()

    query = {
        "metadata.type": "song"
    }

    if name != "":
        query["metadata.name"] = {
            "$regex": re.escape(name),
            "$options": "i"
        }

    if artist != "":
        query["metadata.artist"] = {
            "$regex": re.escape(artist),
            "$options": "i"
        }

    return query


def find_songs():
    return list(db.fs.files.find(build_search_query()).sort("metadata.name", 1))


def print_songs(songs):
    for index, song in enumerate(songs, start=1):
        metadata = song.get("metadata", {})
        print(
            f"{index}. {metadata.get('name')} | "
            f"{metadata.get('artist')} | "
            f"{metadata.get('album')} | "
            f"{metadata.get('genre')} | "
            f"{metadata.get('year')}"
        )


def select_song(songs):
    if len(songs) == 0:
        print("Keine Songs gefunden.")
        return None

    print_songs(songs)

    while True:
        choice = input("Song Nummer: ").strip()

        if choice.isdigit():
            index = int(choice)

            if 1 <= index <= len(songs):
                return songs[index - 1]

        print("Ungueltige Auswahl.")


def add_song():
    print("Song hinzufuegen")

    path = read_required("Audiofile-Pfad")

    if not os.path.exists(path):
        print("Datei wurde nicht gefunden.")
        return

    name = read_required("Name")
    artist = read_required("Interpret")
    album = read_optional("Album")
    genre = read_optional("Genre")
    year = read_optional("Erscheinungsjahr")

    song = Song(name, artist, album, genre, year)

    with open(path, "rb") as file:
        file_id = fs.put(
            file,
            filename=os.path.basename(path),
            metadata=song.to_metadata()
        )

    print("Song wurde gespeichert.")
    print(f"ID: {file_id}")


def update_song():
    print("Song aendern")

    selected = select_song(find_songs())

    if selected is None:
        return

    metadata = selected.get("metadata", {})

    print("Leere Eingabe bedeutet: Wert bleibt gleich.")

    name = input(f"Name ({metadata.get('name', '')}): ").strip()
    artist = input(f"Interpret ({metadata.get('artist', '')}): ").strip()
    album = input(f"Album ({metadata.get('album', '')}): ").strip()
    genre = input(f"Genre ({metadata.get('genre', '')}): ").strip()
    year = input(f"Erscheinungsjahr ({metadata.get('year', '')}): ").strip()
    new_path = input("Neuer Audiofile-Pfad (optional): ").strip()

    new_metadata = {
        "type": "song",
        "name": name or metadata.get("name", ""),
        "artist": artist or metadata.get("artist", ""),
        "album": album or metadata.get("album", ""),
        "genre": genre or metadata.get("genre", ""),
        "year": year or metadata.get("year", "")
    }

    if new_metadata["name"] == "" or new_metadata["artist"] == "":
        print("Name und Interpret duerfen nicht leer sein.")
        return

    if new_path == "":
        db.fs.files.update_one(
            {"_id": selected["_id"]},
            {"$set": {"metadata": new_metadata}}
        )
    else:
        if not os.path.exists(new_path):
            print("Neue Datei wurde nicht gefunden.")
            return

        fs.delete(selected["_id"])

        with open(new_path, "rb") as file:
            fs.put(
                file,
                filename=os.path.basename(new_path),
                metadata=new_metadata
            )

    print("Song wurde geaendert.")


def delete_song():
    print("Song loeschen")

    selected = select_song(find_songs())

    if selected is None:
        return

    metadata = selected.get("metadata", {})
    answer = input(
        f"Song '{metadata.get('name')}' wirklich loeschen? (ja/nein): "
    )

    if answer.strip().lower() != "ja":
        print("Es wurde nichts geloescht.")
        return

    fs.delete(selected["_id"])
    print("Song wurde geloescht.")


def main():
    while True:
        print("\nJukebox Management")
        print("------------------")
        print("1. Song hinzufuegen")
        print("2. Song aendern")
        print("3. Song loeschen")
        print("4. Beenden")

        choice = input("Auswahl: ").strip()

        if choice == "1":
            add_song()
        elif choice == "2":
            update_song()
        elif choice == "3":
            delete_song()
        elif choice == "4":
            break
        else:
            print("Ungueltige Auswahl.")


if __name__ == "__main__":
    main()
