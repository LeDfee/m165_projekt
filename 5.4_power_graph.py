from pymongo import MongoClient
import matplotlib.pyplot as plt


client = MongoClient("mongodb://localhost:27017")

db = client["db_restaurants"]
powers = db["power_logs"]


logs = list(
    powers.find()
    .sort("timestamp", 1)
)

if len(logs) == 0:
    print("Keine Logs vorhanden.")
    exit()


timestamps = []
cpu_values = []
ram_used_values = []

for log in logs:
    timestamps.append(log["timestamp"])
    cpu_values.append(log["cpu"])
    ram_used_values.append(log["ram_used"] / 1024 / 1024)


plt.plot(timestamps, cpu_values, label="CPU in %")
plt.plot(timestamps, ram_used_values, label="RAM in MB")

plt.xlabel("Zeit")
plt.ylabel("Wert")
plt.title("CPU und RAM Auslastung")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()