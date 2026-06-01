from pymongo import MongoClient
from datetime import datetime
import psutil


client = MongoClient("mongodb://localhost:27017")

db = client["db_restaurants"]
powers = db["power_logs"]


class Power:
    def __init__(self, cpu=None, ram_total=None, ram_used=None, timestamp=None):
        if cpu is None:
            self.cpu = psutil.cpu_percent(interval=1)
        else:
            self.cpu = cpu

        if ram_total is None or ram_used is None:
            memory = psutil.virtual_memory()

        if ram_total is None:
            self.ram_total = memory.total
        else:
            self.ram_total = ram_total

        if ram_used is None:
            self.ram_used = memory.used
        else:
            self.ram_used = ram_used

        if timestamp is None:
            self.timestamp = datetime.now()
        else:
            self.timestamp = timestamp

    def to_document(self):
        return {
            "cpu": self.cpu,
            "ram_total": self.ram_total,
            "ram_used": self.ram_used,
            "timestamp": self.timestamp
        }


def delete_old_logs():
    count = powers.count_documents({})

    if count > 10000:
        amount_to_delete = count - 10000

        old_logs = powers.find().sort("timestamp", 1).limit(amount_to_delete)

        old_ids = []

        for log in old_logs:
            old_ids.append(log["_id"])

        powers.delete_many({
            "_id": {
                "$in": old_ids
            }
        })


def main():
    print("Power Logger gestartet...")

    while True:
        power = Power()

        powers.insert_one(power.to_document())

        delete_old_logs()

        print(
            f"{power.timestamp} | "
            f"CPU: {power.cpu}% | "
            f"RAM used: {round(power.ram_used / 1024 / 1024)} MB | "
            f"RAM total: {round(power.ram_total / 1024 / 1024)} MB"
        )


if __name__ == "__main__":
    main()
