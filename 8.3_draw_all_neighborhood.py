from pymongo import MongoClient
from PIL import Image, ImageDraw


client = MongoClient("mongodb://localhost:27017")

db = client["db_restaurants"]
neighborhoods = db["neighborhoods"]


def get_rings(neighborhood):
    geometry = neighborhood.get("geometry", {})
    coordinates = geometry.get("coordinates", [])

    if geometry.get("type") == "Polygon":
        return coordinates

    if geometry.get("type") == "MultiPolygon":
        rings = []

        for polygon in coordinates:
            for ring in polygon:
                rings.append(ring)

        return rings

    return []


def collect_all_coordinates():
    all_coordinates = []

    for neighborhood in neighborhoods.find():
        for ring in get_rings(neighborhood):
            for coordinate in ring:
                all_coordinates.append(coordinate)

    return all_coordinates


def convert_coordinate(lon, lat, min_lon, max_lon, min_lat, max_lat, width, height):
    if max_lon == min_lon:
        x = width // 2
    else:
        x = int((lon - min_lon) / (max_lon - min_lon) * (width - 40)) + 20

    if max_lat == min_lat:
        y = height // 2
    else:
        y = int((max_lat - lat) / (max_lat - min_lat) * (height - 40)) + 20

    return x, y


all_coordinates = collect_all_coordinates()

if len(all_coordinates) == 0:
    print("Keine Koordinaten gefunden.")
    exit()

longitudes = [coord[0] for coord in all_coordinates]
latitudes = [coord[1] for coord in all_coordinates]

min_lon = min(longitudes)
max_lon = max(longitudes)

min_lat = min(latitudes)
max_lat = max(latitudes)

width = 1000
height = 1000

image = Image.new(mode="RGB", size=(width, height), color="white")
draw = ImageDraw.Draw(image)

for neighborhood in neighborhoods.find():
    for ring in get_rings(neighborhood):
        points = []

        for lon, lat in ring:
            point = convert_coordinate(
                lon,
                lat,
                min_lon,
                max_lon,
                min_lat,
                max_lat,
                width,
                height
            )

            points.append(point)

        if len(points) >= 2:
            draw.line(points, fill="black", width=2)

image.show()
image.save("all_neighborhoods.png")
