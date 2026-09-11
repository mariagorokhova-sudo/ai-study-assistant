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

def add_topic(data):
    name = input("Please enter topic name: ").strip()
    if not name:
        print("Topic name cannot be empty!")
        return
    new_topic = {
        "name": name,
        "status": "new",
        "notes": ""
    }
    for topic in data["topics"]:
        if topic["name"] == new_topic["name"]:
            print("This topic already exists!")
            break
    else:
        data["topics"].append(new_topic)

def list_topics(data):
    if not data["topics"]:
        print("No topics yet!")
        return
    for topic in data["topics"]:
        print(topic["name"])

def delete_topic(data):
    name = input("Please enter a topic name: ").strip()
    if not name:
        print("Topic name cannot be empty!")
        return
    for topic in data["topics"]:
        if topic["name"] == name:
            data["topics"].remove(topic)
            save_topics(data)
            break
    else:
        print("Topic is not found!")



data = load_topics()

while True:
    print("\nAI Study Assistant")
    print("1. List topics")
    print("2. Add topic")
    print("3. Delete topic")
    print("4. Exit")

    choice = input("Please choose an option: ").strip()

    if choice == "1":
        list_topics(data)
    elif choice == "2":
        add_topic(data)
        save_topics(data)
    elif choice == "3":
        delete_topic(data)
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid option!")
    