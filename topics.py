import storage
import conversations

def load_data():
    return storage.load_data()


def add_topic(data, name):
    name = name.strip()
    if not name:
        return False, "empty"
    new_topic = {
        "name": name,
        "course_statuses": {},
        "notes": []
    }
    for topic in data["topics"]:
        if topic["name"].lower() == new_topic["name"].lower():
            return False, "duplicate"

    data["topics"].append(new_topic)
    storage.save_data(data)
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
        if topic["name"].lower() == name.lower():
            for conversation in data["conversations"]:
                if conversation["topic"].lower() == topic["name"].lower():
                    return False, "topic has conversations"
            data["topics"].remove(topic)
            storage.save_data(data)
            return True, "deleted"
    return False, "not found"


def add_note(data, topic_name, new_note):
    if not new_note.strip():
        return False, "empty note"
    for entry in data["topics"]:
        if topic_name.lower() == entry["name"].lower():
            entry["notes"].append(new_note.strip())
            storage.save_data(data)
            return True, "added"
    return False, "topic not found"


def get_notes(data, topic_name):
    for entry in data["topics"]:
        if topic_name.lower() == entry["name"].lower():
            return entry["notes"]


def delete_note(data, topic_name, note_index):
    for topic in data["topics"]:
        if topic["name"].lower() == topic_name.lower():
            if note_index < 0 or note_index >= len(topic["notes"]):
                return False, "incorrect index"
            topic["notes"].pop(note_index)
            storage.save_data(data)
            return True, "deleted"
    return False, "topic not found"


def assign_topic_to_course(data, topic_name, course_code):
    course_code = course_code.strip().upper()
    topic_name = topic_name.strip()
    if not course_code or not topic_name:
        return False, "empty field"
    course_exists = any(
        entry["code"].lower() == course_code.lower()
        for entry in data["courses"]
    )
    if not course_exists:
        return False, "course not found"
    for entry in data["topics"]:
        if entry["name"].lower() == topic_name.lower():
            entry.setdefault("course_statuses", {})
            if course_code in entry["course_statuses"]:
                return False, "duplicate"
            entry["course_statuses"][course_code] = "learning"
            storage.save_data(data)
            return True, "assigned"
    return False, "topic not found"


def change_topic_course_status(data, topic_name, course_code, new_status):
    course_code = course_code.strip().upper()
    topic_name = topic_name.strip()
    new_status = new_status.strip().lower()
    if not topic_name or not course_code:
        return False, "empty field"
    if new_status not in ("learning", "exam prep", "finished"):
        return False, "invalid status"
    for entry in data["topics"]:
        if entry["name"].lower() == topic_name.lower():
            if course_code not in entry.get("course_statuses", {}):
                return False, "topic not assigned"
            entry["course_statuses"][course_code] = new_status
            storage.save_data(data)
            return True, "changed"
    return False, "topic not found"


def unassign_topic_from_course(data, topic_name, course_code):
    course_code = course_code.strip().upper()
    topic_name = topic_name.strip()
    if not course_code or not topic_name:
        return False, "empty field"
    for entry in data["topics"]:
        if entry["name"].lower() == topic_name.lower():
            if course_code not in entry.get("course_statuses", {}):
                return False, "topic not assigned"
            del entry["course_statuses"][course_code]
            storage.save_data(data)
            return True, "unassigned"
    return False, "topic not found"


def get_topics_for_course(data, course_code):
    course_code = course_code.strip().upper()
    statuses_list = ["learning", "exam prep", "finished"]
    topics_list = []
    for status in statuses_list:
        for entry in data["topics"]:
            if (entry.get("course_statuses", {})).get(course_code) == status:
                topics_list.append(entry)
    return topics_list


def show_topics_for_course(data, course_code, include_back=False):
    if not data["topics"]:
        print("No topics yet!\n")
        return
    course_code = course_code.strip().upper()
    course_topics = get_topics_for_course(data, course_code)
    if not course_topics:
        print("No topics assigned to this course!\n")
        return
    statuses = ("learning", "exam prep", "finished")
    topic_number = 1
    for status in statuses:
        if not any(
            topic["course_statuses"][course_code] == status
            for topic in course_topics
        ):
           continue 
        print(f'{status}:')
        for topic in course_topics:
            if topic["course_statuses"][course_code] == status:
                print(f'{topic_number}. {topic["name"]}')
                topic_number += 1
                print()
    if include_back:
        print(f'{topic_number}. Back')
        print()


def show_topic_card(data, topic_entry):
    print("\n==============================================")
    print(f'Topic: {topic_entry["name"]}')
    print("==============================================\n")
    if not topic_entry["course_statuses"]:
        print("Courses: not assigned!\n")
    else:
        print("Courses:\n")
        for course_code, status in topic_entry["course_statuses"].items():
            for course in data["courses"]:
                if course["code"].lower() == course_code.lower():
                    print(f'{course_code} - {course["name"]} - status: {status}.')
    print("-----------------------------------------------------------------------------------")
    print(f'Notes: {len(topic_entry["notes"])}\n')
    for note in topic_entry["notes"]:
        print(f'- {note[:30]}...')
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("-----------------------------------------------------------------------------------")
    conversations_count = 0
    conversations_list = []
    for conversation in data["conversations"]:
        if conversation["topic"].lower() == topic_entry["name"].lower():
            conversations_count += 1
            conversations_list.append(conversation)
    print(f'Conversations: {conversations_count}\n')
    for conversation in conversations_list:
        last_user_message = conversations.get_last_user_message(conversation)
        print(f'Topic: {conversation["topic"]} | AI mode: {conversation["ai_mode"]} | Last question: {last_user_message}')
        print("-----------------------------------------------------------------------------------")