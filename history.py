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

def count_history_by_topics(data):
    counts = {}

    for entry in data["history"]:
        topic = entry["topic"]
        if topic in counts:
            counts[topic] += 1
        else:
            counts[topic] = 1

    return counts

def sort_topics_counts_descending(counts):
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))

def get_unique_history_topics(data):
    unique_topics = set()
    for entry in data['history']:
        unique_topics.add(entry["topic"])
    return unique_topics
