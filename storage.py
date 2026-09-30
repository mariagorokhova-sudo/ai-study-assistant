import json
from pathlib import Path

DATA_FILE = Path("topics.json")

def load_topics():
    if DATA_FILE.exists():
        try:
            with DATA_FILE.open("r") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError("Invalid JSON file") from error
        required_topic_keys = {"name", "status", "notes"}
        required_conversation_keys = {"topic", "ai_mode", "messages"}
        required_message_keys = {"role", "content"}
        if (
            not isinstance(data, dict) 
            or not isinstance(data.get("topics"), list) 
            or not isinstance(data.get("conversations"), list)
            or not all(isinstance(topic, dict) for topic in data["topics"])
            or not all(required_topic_keys.issubset(topic) for topic in data["topics"])
            or not all(isinstance(topic["name"], str) for topic in data["topics"])
            or not all(isinstance(topic["notes"], list) for topic in data["topics"])
            or not all(all(isinstance(note, str) for note in topic["notes"]) for topic in data["topics"])
            or not all(isinstance(topic["status"], str) for topic in data["topics"])
            or not all(isinstance(conversation, dict) for conversation in data["conversations"])
            or not all(required_conversation_keys.issubset(conversation) for conversation in data["conversations"])
            or not all(isinstance(conversation["topic"], str) for conversation in data["conversations"])
            or not all(isinstance(conversation["ai_mode"], str) for conversation in data["conversations"])
            or not all(isinstance(conversation["messages"], list) for conversation in data["conversations"])
            or not all(all(isinstance(message, dict) for message in conversation["messages"]) for conversation in data["conversations"])
            or not all(all(required_message_keys.issubset(message) for message in conversation["messages"]) for conversation in data["conversations"])
            or not all(all(isinstance(message["role"], str) for message in conversation["messages"]) for conversation in data["conversations"])
            or not all(all(isinstance(message["content"], str) for message in conversation["messages"]) for conversation in data["conversations"])
        ):
            raise ValueError("Invalid data structure.")
        return data
    return {"topics":[], "conversations": []}

def save_topics(data):
    with DATA_FILE.open("w") as file:
        json.dump(data, file, indent=2)

