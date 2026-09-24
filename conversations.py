def create_conversation(data, topic, ai_mode):
    conversation_entry = {"topic": topic, "ai_mode": ai_mode, "messages": []}
    data["conversations"].append(conversation_entry)
    return conversation_entry

def add_message_to_conversation(conversation_entry, role, content):
    conversation_entry["messages"].append({"role": role, "content": content})

def get_conversations_by_topic(data, topic_name):
    conversations_list = []
    for entry in data["conversations"]:
        if entry["topic"].lower() == topic_name.lower():
            conversations_list.append(entry)
    return conversations_list

def get_last_user_message(conversation_entry):
    for message in reversed(conversation_entry["messages"]):
        if message["role"] == "user":
            return message["content"]
    