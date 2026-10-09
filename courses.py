import storage
import topics

def add_course(data, code, course_name, session):
    code = code.strip().upper()
    course_name = course_name.strip()
    session = session.strip()
    if not code or not course_name or not session:
        return False, "empty field"
    for entry in data["courses"]:
        if code.lower() == entry["code"].lower():
            return False, "duplicate"
    course_entry = {
        "code": code,
        "name": course_name,
        "session": session,
        "status": "active"
    }
    data["courses"].append(course_entry)
    storage.save_data(data)
    return True, "added"


def list_courses(data, status=None):
    if status is None:
        return data["courses"]
    courses_list = []
    for entry in data["courses"]:
        if entry["status"] == status:
            courses_list.append(entry)
    return courses_list


def edit_course(data, code, field_name, new_value):
    code = code.strip().upper()
    field_name = field_name.strip()
    new_value = new_value.strip()
    if not code or not field_name or not new_value:
        return False, "empty field"
    if field_name not in ("name", "session"):
        return False, "invalid field"
    for entry in data["courses"]:
        if entry["code"].lower() == code.lower():
            entry[field_name] = new_value
            storage.save_data(data)
            return True, "updated"
    return False, "course not found"


def change_course_status(data, code, new_status):
    code = code.strip().upper()
    new_status = new_status.strip().lower()
    if not code or not new_status:
        return False, "empty field"
    if new_status not in ("active", "finished"):
        return False, "invalid status"
    for entry in data["courses"]:
        if entry["code"].lower() == code.lower():
            entry["status"] = new_status
            storage.save_data(data)
            return True, "updated"
    return False, "course not found"


def delete_course(data, course_code):
    course_code = course_code.strip().upper()
    if not course_code:
        return False, "empty field"
    for entry in data["courses"]:
        if entry["code"].lower() == course_code.lower():
            for topic in data["topics"]:
                if course_code in topic.get("course_statuses", {}):
                    return False, "course has topics"
            data["courses"].remove(entry)
            storage.save_data(data)
            return True, "deleted"
    return False, "course not found"


def show_course_card(data, course_entry):
    course_topics_list = topics.get_topics_for_course(data, course_entry["code"])
    course_topic_count = len(course_topics_list)
    learning_count = 0
    exam_prep_count = 0
    finished_count = 0
    for topic in course_topics_list:
        topic_status = topic["course_statuses"][course_entry["code"]]
        if  topic_status == "learning":
            learning_count += 1
        elif topic_status == "exam prep":
            exam_prep_count += 1
        elif topic_status == "finished":
            finished_count += 1
    print("\n==============================================")
    print(f'{course_entry["code"]} - {course_entry["name"]}')
    print("==============================================\n")
    print(f'Session: {course_entry["session"]}')
    print(f'Status: {course_entry["status"]}')
    print(f'Topics: {course_topic_count}\n')
    print(f'learning: {learning_count}')
    print(f'exam prep: {exam_prep_count}')
    print(f'finished: {finished_count}')