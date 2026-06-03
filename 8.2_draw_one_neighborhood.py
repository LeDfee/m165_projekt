from pymongo import MongoClient
from PIL import Image, ImageDraw


client = MongoClient("mongodb://localhost:27017")

db = client["db_restaurants"]
neighborhoods = db["neighborhoods"]


def get_first_ring(neighborhood):
    geometry = neighborhood.get("geometry", {})
    coordinates = geometry.get("coordinates", [])

    if geometry.get("type") == "Polygon":
        return coordinates[0]

    if geometry.get("type") == "MultiPolygon":
        return coordinates[0][0]

    return []


def convert_coordinates_to_points(coordinates, width, height):
    longitudes = [coord[0] for coord in coordinates]
    latitudes = [coord[1] for coord in coordinates]

    min_lon = min(longitudes)
    max_lon = max(longitudes)

    min_lat = min(latitudes)
    max_lat = max(latitudes)

    points = []

    for lon, lat in coordinates:
        if max_lon == min_lon:
            x = width // 2
        else:
            x = int((lon - min_lon) / (max_lon - min_lon) * (width - 40)) + 20

        if max_lat == min_lat:
            y = height // 2
        else:
            y = int((max_lat - lat) / (max_lat - min_lat) * (height - 40)) + 20

        points.append((x, y))

    return points


neighborhood = neighborhoods.find_one()

if neighborhood is None:
    print("Kein Neighborhood gefunden.")
    exit()

coordinates = get_first_ring(neighborhood)

if len(coordinates) == 0:
    print("Kein Polygon gefunden.")
    exit()

width = 800
height = 800

image = Image.new(mode="RGB", size=(width, height), color="white")
draw = ImageDraw.Draw(image)

points = convert_coordinates_to_points(coordinates, width, height)

if len(points) >= 2:
    draw.line(points, fill="blue", width=2)
else:
    print("Zu wenig Koordinaten zum Zeichnen.")

image.show()
image.save("one_neighborhood.png")
