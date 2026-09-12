import json
from pathlib import Path

DATA_FILE = Path("topics.json")

def load_topics():
    if DATA_FILE.exists():
        with DATA_FILE.open("r") as file:
            return json.load(file)

    return {"topics":[]}

def save_topics(data):
    with DATA_FILE.open("w") as file:
        json.dump(data, file, indent=2)