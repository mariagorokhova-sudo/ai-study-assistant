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

def get_unique_conversations_topics(data):
    conversation_topics_list = []
    for conversation_entry in data["conversations"]:
        if conversation_entry["topic"] not in conversation_topics_list:
            conversation_topics_list.append(conversation_entry["topic"])
    return conversation_topics_list

def count_conversations_by_topic(data):
    counts = {}
    for entry in data["conversations"]:
        topic = entry["topic"]
        matching_topic = find_matching_topic_case_insensitive(topic, counts)
        if matching_topic is None:
            counts[topic] = 1
        else:
            counts[matching_topic] += 1
    return counts

def find_matching_topic_case_insensitive(topic, existing_topics):
    for existing_topic in existing_topics:
        if topic.lower() == existing_topic.lower():
            return existing_topic
    
def sort_conversations_counts_descending(counts):
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))