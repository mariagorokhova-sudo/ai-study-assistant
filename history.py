import storage

def add_history_entry(data, topic, question, answer):
    entry = {
        "topic": topic,
        "question": question,
        "answer": answer
    }
    data["history"].append(entry)
    storage.save_topics(data)

def list_history_entries(data):
    return data["history"]

def get_history_by_topic(data, topic):
    filtered_history = []
    for entry in data["history"]:
        if entry["topic"] == topic:
            filtered_history.append(entry)

    return filtered_history
