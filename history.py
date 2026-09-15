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
