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
        if entry["topic"].lower() == topic.lower():
            filtered_history.append(entry)

    return filtered_history

def count_history_by_topics(data):
    counts = {}

    for entry in data["history"]:
        topic = entry["topic"]
        matching_topic = find_matching_topic_case_insensitive(topic, counts)
        if matching_topic is None:
            counts[topic] = 1
        else:
            counts[matching_topic] += 1

    return counts

def sort_topics_counts_descending(counts):
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))

def get_unique_history_topics(data):
    unique_topics = set()
    for entry in data['history']:
        topic = entry["topic"]
        if find_matching_topic_case_insensitive(topic, unique_topics) is None:
            unique_topics.add(topic)
    return unique_topics

def find_matching_topic_case_insensitive(topic, existing_topics):
    for existing_topic in existing_topics:
        if topic.lower() == existing_topic.lower():
            return existing_topic
    
