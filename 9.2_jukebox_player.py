from pymongo import MongoClient
import gridfs
import os
import random
import re
import subprocess
import tempfile


client = MongoClient("mongodb://localhost:27017")

db = client["jukebox"]
fs = gridfs.GridFS(db)
playlist = []


def add_regex_filter(query, field, value):
    if value != "":
        query[f"metadata.{field}"] = {
            "$regex": re.escape(value),
            "$options": "i"
        }


def search_songs():
    name = input("Name: ").strip()
    artist = input("Interpret: ").strip()
    album = input("Album: ").strip()
    genre = input("Genre: ").strip()

    query = {
        "metadata.type": "song"
    }

    add_regex_filter(query, "name", name)
    add_regex_filter(query, "artist", artist)
    add_regex_filter(query, "album", album)
    add_regex_filter(query, "genre", genre)

    return list(db.fs.files.find(query).sort("metadata.name", 1))


def print_songs(songs):
    for index, song in enumerate(songs, start=1):
        metadata = song.get("metadata", {})
        print(
            f"{index}. {metadata.get('name')} | "
            f"{metadata.get('artist')} | "
            f"{metadata.get('album')} | "
            f"{metadata.get('genre')}"
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


def add_to_playlist():
    songs = search_songs()
    selected = select_song(songs)

    if selected is None:
        return

    playlist.append(selected["_id"])
    print("Song wurde zur Playlist hinzugefuegt.")


def open_audio_file(path):
    if os.name == "nt":
        os.startfile(path)
    elif os.name == "posix":
        subprocess.Popen(["xdg-open", path])
    else:
        print(f"Audiofile wurde gespeichert: {path}")


def play_song(song_id):
    stored_file = fs.get(song_id)
    suffix = os.path.splitext(stored_file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(stored_file.read())
        temp_path = temp_file.name

    metadata = stored_file.metadata
    print(f"Spiele: {metadata.get('name')} - {metadata.get('artist')}")
    open_audio_file(temp_path)


def play_next():
    if len(playlist) > 0:
        song_id = playlist.pop(0)
        play_song(song_id)
        return

    songs = list(db.fs.files.find({"metadata.type": "song"}))

    if len(songs) == 0:
        print("Keine Songs vorhanden.")
        return

    song = random.choice(songs)
    play_song(song["_id"])


def show_playlist():
    if len(playlist) == 0:
        print("Playlist ist leer.")
        return

    print("Playlist:")

    for index, song_id in enumerate(playlist, start=1):
        song = db.fs.files.find_one({"_id": song_id})

        if song is None:
            print(f"{index}. Song wurde nicht gefunden.")
            continue

        metadata = song.get("metadata", {})
        print(f"{index}. {metadata.get('name')} - {metadata.get('artist')}")


def main():
    while True:
        print("\nJukebox Player")
        print("--------------")
        print("1. Song suchen und zur Playlist hinzufuegen")
        print("2. Naechsten Song spielen")
        print("3. Playlist anzeigen")
        print("4. Beenden")

        choice = input("Auswahl: ").strip()

        if choice == "1":
            add_to_playlist()
        elif choice == "2":
            play_next()
        elif choice == "3":
            show_playlist()
        elif choice == "4":
            break
        else:
            print("Ungueltige Auswahl.")


if __name__ == "__main__":
    main()
