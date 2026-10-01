import storage

def load_data():
    return storage.load_data()


def add_topic(data, name):
    name = name.strip()
    if not name:
        return False, "empty"
    new_topic = {
        "name": name,
        "status": "new",
        "notes": []
    }
    for topic in data["topics"]:
        if topic["name"].lower() == new_topic["name"].lower():
            return False, "duplicate"

    data["topics"].append(new_topic)
    storage.save_data(data)
    return True, "added"


def list_topics(data):
    topic_names = []
    for topic in data["topics"]:
        topic_names.append(topic["name"])
    return topic_names


def delete_topic(data, name):
    name = name.strip()
    if not name:
        return False, "empty"
    for topic in data["topics"]:
        if topic["name"].lower() == name.lower():
            data["topics"].remove(topic)
            storage.save_data(data)
            return True, "deleted"
    return False, "not found"


def change_topic_status(data, topic_name, new_status):
    new_status = new_status.strip().lower()
    valid_statuses = {"new", "in progress", "exam prep", "finished"}
    if new_status not in valid_statuses:
        return False, "invalid status"
    for entry in data["topics"]:
        if entry["name"].lower() == topic_name.lower():
            entry["status"] = new_status
            storage.save_data(data)
            return True, "changed"
    return False, "topic not found"


def add_note(data, topic_name, new_note):
    if not new_note.strip():
        return False, "empty note"
    for entry in data["topics"]:
        if topic_name.lower() == entry["name"].lower():
            entry["notes"].append(new_note.strip())
            storage.save_data(data)
            return True, "added"
    return False, "topic not found"


def get_notes(data, topic_name):
    for entry in data["topics"]:
        if topic_name.lower() == entry["name"].lower():
            return entry["notes"]


def delete_note(data, topic_name, note_index):
    for topic in data["topics"]:
        if topic["name"].lower() == topic_name.lower():
            if note_index < 0 or note_index >= len(topic["notes"]):
                return False, "incorrect index"
            topic["notes"].pop(note_index)
            storage.save_data(data)
            return True, "deleted"
    return False, "topic not found"