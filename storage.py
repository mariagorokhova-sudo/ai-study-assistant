import json
from pathlib import Path

DATA_FILE = Path("topics.json")

def load_topics():
    if DATA_FILE.exists():
        with DATA_FILE.open("r") as file:
            data = json.load(file)
            return data
    return {"topics":[], "conversations": []}

def save_topics(data):
    with DATA_FILE.open("w") as file:
        json.dump(data, file, indent=2)

