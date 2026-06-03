from pymongo import MongoClient
import gridfs
import os

client = MongoClient("mongodb://localhost:27017")

db = client["files"]
fs = gridfs.GridFS(db)

path = input("File: ")

if not os.path.exists(path):
    print("File not found")
    exit()

# Save
with open(path, "rb") as file:
    file_id = fs.put(file, filename=os.path.basename(path))

print("File saved")
print(f"File ID: {file_id}")

# Read / Restore
file = fs.get(file_id)
restore_path = os.path.join(".", "restored_" + file.filename)

data = file.read()

with open(restore_path, "wb") as file:
    file.write(data)

print("File restored")
print(f"Restore path: {restore_path}")
