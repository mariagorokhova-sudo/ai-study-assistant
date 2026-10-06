import courses
import menu_utils
import topics

def manage_courses_menu(data):
    while True:
        print("\n===========================")
        print("Current list of courses:")
        print("===========================\n")
        courses_list = courses.list_courses(data)
        course_options = [
            f'{course["code"]} - {course["name"]}'
            for course in courses_list
        ]
        course_options.extend(["Add course", "Back"])
        menu_utils.print_numbered_list(course_options)
        courses_choice = menu_utils.choose_from_numbered_list(course_options, prompt="Please choose a course to view details or add a new one: ", return_index=True)
        if courses_choice is None:
            continue

        if courses_choice == len(course_options) - 1:
            break

        elif courses_choice == len(course_options) - 2:
            print("You've chosen to add a course.\n")
            course_code = input("Please enter a course code: ")
            course_name = input("Please enter a course name: ")
            session = input("Please enter a course session: ")
            added, reason = courses.add_course(data, course_code, course_name, session)
            if added:
                print(f'\nCourse {course_code} - {course_name} is successfully added!\n')
            elif reason == "empty field":
                print("\nCourse fields cannot be empty!\n")
            elif reason == "duplicate":
                print("\nThis course already exists!\n")
            continue

        
        else:
            while True:
                course = courses_list[courses_choice]
                courses.show_course_card(data, course)
                course_actions = [
                    "View topics",
                    "Assign topic",
                    "Change topic status",
                    "Unassign topic",
                    "Edit course",
                    "Change course status",
                    "Delete course",
                    "Back"
                ]
                print("\n=================================")
                print("Actions available for this course:")
                print("=================================\n")
                menu_utils.print_numbered_list(course_actions)
                action_choice = menu_utils.choose_from_numbered_list(course_actions, prompt="Please choose your action from the list above: ")

                if action_choice == "View topics":
                    print(f'You have chosen to view all topics assigned to the course {course["code"]} - {course["name"]}.\n')
                    topics.show_topics_for_course(data, course["code"])

                elif action_choice == "Assign topic":
                    print(f'You have chosen to assign a topic to the course {course["code"]} - {course["name"]}.\n')
                    topics_list = [topic["name"] for topic in data["topics"] if course["code"] not in topic.get("course_statuses", {})]
                    if not topics_list:
                        print("No topics available for assignment!\n")
                        continue
                    menu_utils.print_numbered_list(topics_list)
                    topic_name = menu_utils.choose_from_numbered_list(topics_list, prompt="Please choose a topic to assign: ")
                    if topic_name is None:
                        continue
                    assigned, reason = topics.assign_topic_to_course(data, topic_name, course["code"])
                    if assigned:
                        print(f'Topic {topic_name} has been assigned to the course {course["code"]} - {course["name"]}.\n')

                elif action_choice == "Change topic status":
                    print("You've chosen to change topic status.")
                    topics_list = topics.get_topics_for_course(data, course["code"])
                    if not topics_list:
                        print("No topics assigned to this course!\n")
                        continue
                    topic_names = [topic["name"] for topic in topics_list]
                    print("\n=============================================")
                    print("Current list of topics assigned to the course:")
                    print("=============================================\n")
                    menu_utils.print_numbered_list(topic_names)
                    topic = menu_utils.choose_from_numbered_list(topics_list, prompt="Please choose a topic to change satus: ")
                    if topic is None:
                        continue
                    current_status = topic["course_statuses"][course["code"]]
                    statuses = ["learning", "exam prep", "finished"]
                    available_statuses = [status for status in statuses if status != current_status]
                    print("List of available statuses:\n")
                    menu_utils.print_numbered_list(available_statuses)
                    new_status = menu_utils.choose_from_numbered_list(available_statuses, prompt="Please choose a new status: ")
                    if new_status is None:
                        continue
                    changed, reason = topics.change_topic_course_status(data, topic["name"], course["code"], new_status)
                    if changed:
                        print(f'Status of topic {topic["name"]} is changed to {new_status}!\n')

                elif action_choice == "Unassign topic":
                    print(f'You have chosen to unassign a topic from the course {course["code"]} - {course["name"]}.\n')
                    topics_list = topics.get_topics_for_course(data, course["code"])
                    if not topics_list:
                        print("No topics assigned to this course!\n")
                        continue
                    topic_names = [topic["name"] for topic in topics_list]
                    print("\n=============================================")
                    print("Current list of topics assigned to the course:")
                    print("=============================================\n")
                    menu_utils.print_numbered_list(topic_names)
                    topic_name = menu_utils.choose_from_numbered_list(topic_names, prompt="Please choose a topic to unassign: ")
                    if topic_name is None:
                        continue
                    unassigned, reason = topics.unassign_topic_from_course(data, topic_name, course["code"])
                    if unassigned:
                        print(f'Topic {topic_name} has been unassigned from course {course["code"]} - {course["name"]}.\n')

                elif action_choice == "Edit course":
                    print(f'You have chosen to edit course {course["code"]} - {course["name"]} details.\n')
                    options_list = ["name", "session"]
                    print("Fields available to change:\n")
                    menu_utils.print_numbered_list(options_list)
                    field_name = menu_utils.choose_from_numbered_list(options_list, prompt="Please choose a field to change: ")
                    if field_name is None:
                        continue
                    new_value = input("Please enter a new value for this field: ")
                    updated, reason = courses.edit_course(data, course["code"], field_name, new_value)
                    if updated:
                        print(f'Course {course["code"]} {field_name} has been changed to {new_value}.\n')
                    elif reason == "empty field":
                        print("New value cannot be empty!\n")

                elif action_choice == "Change course status":
                    print(f'You have chosen to change the status of the course {course["code"]} - {course["name"]}.\n')
                    if course["status"] == "active":
                        new_status = "finished"
                    else:
                        new_status = "active"
                    updated, reason = courses.change_course_status(data, course["code"], new_status)
                    if updated:
                        print(f'Course {course["code"]} - {course["name"]} has been changed to {new_status}.\n')

                elif action_choice == "Delete course":
                    print(f'You have chosen to delete the course {course["code"]} - {course["name"]}.\n')
                    confirmation = input(f'Please confirm you would like to delete course {course["code"]} - {course["name"]}: Y/N?').strip().lower()
                    if confirmation == "y":
                        deleted, reason = courses.delete_course(data, course["code"])
                        if deleted:
                            print(f'Course {course["code"]} - {course["name"]} has been deleted.\n')
                            break
                        elif reason == "course has topics":
                            print("This course has topics assigned, not possible to delete.\n")
                    else:
                        print("Course is not deleted!\n")
                        continue


                elif action_choice == "Back":
                    break