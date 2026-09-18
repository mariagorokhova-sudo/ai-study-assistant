import json
from pathlib import Path

DATA_FILE = Path("topics.json")

def load_topics():
    if DATA_FILE.exists():
        with DATA_FILE.open("r") as file:
            data = json.load(file)
            data.setdefault("history", [])
            for entry in data["topics"]:
                if entry["notes"] == "":
                    entry["notes"] = []
            return data
    return {"topics":[], "history": []}

def save_topics(data):
    with DATA_FILE.open("w") as file:
        json.dump(data, file, indent=2)

