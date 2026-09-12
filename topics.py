import storage

def load_data():
    return storage.load_topics()

def add_topic(data, name):
    name = name.strip()
    if not name:
        return False, "empty"
    new_topic = {
        "name": name,
        "status": "new",
        "notes": ""
    }
    for topic in data["topics"]:
        if topic["name"] == new_topic["name"]:
            return False, "duplicate"

    data["topics"].append(new_topic)
    storage.save_topics(data)
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
        if topic["name"] == name:
            data["topics"].remove(topic)
            storage.save_topics(data)
            return True, "deleted"
    return False, "not found"
