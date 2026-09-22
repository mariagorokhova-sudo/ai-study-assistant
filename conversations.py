def create_conversation(data, topic, ai_mode):
    conversation_entry = {"topic": topic, "ai_mode": ai_mode, "messages": []}
    data["conversations"].append(conversation_entry)
    return conversation_entry

def add_message_to_conversation(conversation_entry, role, content):
    conversation_entry["messages"].append({"role": role, "content": content})
    