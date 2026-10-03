import storage

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