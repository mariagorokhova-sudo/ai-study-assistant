import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data.json"

def is_valid_topics(topics):
    required_topic_keys = {"name", "status", "notes"}
    return (
        isinstance(topics, list)
        and all(isinstance(topic, dict) for topic in topics)
        and all(required_topic_keys.issubset(topic) for topic in topics)
        and all(isinstance(topic["name"], str) for topic in topics)
        and all(isinstance(topic["notes"], list) for topic in topics)
        and all(all(isinstance(note, str) for note in topic["notes"]) for topic in topics)
        and all(isinstance(topic["status"], str) for topic in topics)
    )


def is_valid_conversations(conversations):
    required_conversation_keys = {"topic", "ai_mode", "messages"}
    required_message_keys = {"role", "content"}
    return (
        isinstance(conversations, list)
        and all(isinstance(conversation, dict) for conversation in conversations)
        and all(required_conversation_keys.issubset(conversation) for  conversation in conversations)
        and all(isinstance(conversation["topic"], str) for  conversation in conversations)
        and all(isinstance(conversation["ai_mode"], str) for  conversation in conversations)
        and all(isinstance(conversation["messages"], list) for  conversation in conversations)
        and all(all(isinstance(message, dict) for message in conversation["messages"]) for conversation in conversations)
        and all(
            all(
                required_message_keys.issubset(message)
                for message in conversation["messages"])
                for conversation in conversations
                )
        and all(
            all(
                isinstance(message["role"], str)
                for message in conversation["messages"])
                for conversation in conversations
                )
        and all(
            all(
                isinstance(message["content"], str)
                for message in conversation["messages"])
                for conversation in conversations
                )
    )


def load_data():
    if DATA_FILE.exists():
        try:
            with DATA_FILE.open("r") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError("Invalid JSON file") from error
        if (
            not isinstance(data, dict) 
            or not is_valid_topics(data.get("topics"))
            or not is_valid_conversations(data.get("conversations"))
        ):
            raise ValueError("Invalid data structure.")
        return data
    return {"topics":[], "conversations": []}


def save_data(data):
    temporary_data = DATA_FILE.with_suffix(".tmp")
    try:
        with temporary_data.open("w") as file:
            json.dump(data, file, indent=2)
        temporary_data.replace(DATA_FILE)
    finally:
        if temporary_data.exists():
            temporary_data.unlink()