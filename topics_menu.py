import topics
import menu_utils
import conversations
import courses_menu
import conversations_menu

def manage_topics_menu(data):
    while True:
        topics_menu_list = topics.list_topics(data)
        topics_menu_list.extend(["Add topic", "Back"])
        topics_menu_options = data["topics"].copy()
        topics_menu_options.extend(["Add topic", "Back"])
        print("\n===========================")
        print("Current list of topics:")
        print("===========================\n")
        menu_utils.print_numbered_list(topics_menu_list)
        print("===================================================================================")
        topics_choice = menu_utils.choose_from_numbered_list(topics_menu_options, prompt="Please choose a topic to view details or add a new one: ")
        if topics_choice is None:
            continue

        if topics_choice == "Add topic":
            print("You've chosen to add topic.")
            topic_name = input("Please enter a topic name: ")
            print(f"\nYou've entered: {topic_name}")
            added, reason = topics.add_topic(data, topic_name)
            if added:
                print("Topic added!")
            elif reason == "empty":
                print("Topic could not be empty!\n")
            elif reason == "duplicate":
                print("Topic already exists!\n")

        elif topics_choice == "Back":
            break

        else:
            print(f'You have chosen to view details of topic {topics_choice["name"]}.\n')
            manage_topic_details_menu(data, topics_choice)


def manage_topic_details_menu(data, topic_entry):
    while True:
        topics.show_topic_card(data, topic_entry)
        print("\n=================================")
        print("Actions available for this topic:")
        print("=================================\n")
        actions_list = [
            "View notes",
            "Add note",
            "Delete note",
            "Change status",
            "View conversations",
            "View courses",
            "Delete topic",
            "Back"
            ]
        menu_utils.print_numbered_list(actions_list)
        topic_details_choice = menu_utils.choose_from_numbered_list(actions_list, prompt="Please choose your action from the list above: ")
        
        if topic_details_choice == "View notes":
            print("You've chosen to view all topic notes.\n")
            if not topic_entry["notes"]:
                print("No notes for this topic yet!\n")
                continue
            print("\n==================================================================================")
            print("Current list of notes:")
            print("==================================================================================\n")
            menu_utils.print_numbered_list(topic_entry["notes"], separator=True)
        
        elif topic_details_choice == "Add note":
            print("You've chosen to add a note to the topic.\n")
            new_note = input("Please enter your note: ")
            added, reason = topics.add_note(data, topic_entry["name"], new_note)
            if added:
                print("Note added!\n")
            elif reason == "empty note":
                print("It's not possible to add an empty note!\n")

        elif topic_details_choice == "Delete note":
            print("you've chosen to delete a note from the topic.\n")
            print("\n==================================================================================")
            print("Current list of notes:")
            print("==================================================================================\n")
            if not topic_entry["notes"]:
                print("No notes for this topic yet!\n")
                continue
            menu_utils.print_numbered_list(topic_entry["notes"], separator=True)
            note_index = menu_utils.choose_from_numbered_list(topic_entry["notes"],
                                                              prompt="Please choose a note to delete: ",
                                                              return_index=True)
            if note_index is None:
                continue
            confirmation = input("Please confirm you would like to delete this note: Y/N? ").strip().lower()
            if confirmation == "y":
                deleted, reason = topics.delete_note(data, topic_entry["name"], note_index)
                if deleted:
                    print("Note deleted!\n")
                elif reason == "incorrect index":
                    print("Impossible to delete, note index is incorrect.\n")
            else:
                print("Note is not deleted!\n")

        elif topic_details_choice == "Change status":
            if not topic_entry["course_statuses"]:
                print("This topic is not assigned to any course!\n")
                continue
            codes_list = []
            course_labels = []
            for course_code, status in topic_entry["course_statuses"].items():
                codes_list.append(course_code)
                for course in data["courses"]:
                    if course["code"].lower() == course_code.lower():
                        course_labels.append(f'{course_code} - {course["name"]} - status: {status}')
            print("\n==================================================================================")
            print("Current list of courses this topic is assigned to:")
            print("==================================================================================\n")
            menu_utils.print_numbered_list(course_labels)
            course_code_choice = menu_utils.choose_from_numbered_list(codes_list, prompt="Please choose a course to change topic status for: ")
            if not course_code_choice:
                continue
            current_status = topic_entry["course_statuses"][course_code_choice]
            statuses = ["learning", "exam prep", "finished"]
            available_statuses = [status for status in statuses if status != current_status]
            print("List of available statuses:\n")
            menu_utils.print_numbered_list(available_statuses)
            new_status = menu_utils.choose_from_numbered_list(available_statuses, prompt="Please choose a new status: ")
            if new_status is None:
                continue
            changed, reason = topics.change_topic_course_status(data, topic_entry["name"], course_code_choice, new_status)
            if changed:
                print(f'Topic status has been changed!\n')

        elif topic_details_choice == "View conversations":
            conversations_list = conversations.get_conversations_by_topic(data, topic_entry["name"])
            if not conversations_list:
                print("No conversations for this topic yet!\n")
                continue
            menu_utils.print_numbered_conversations(conversations_list, include_back_option=True)
            conversations_list.extend(["Back"])
            conversation_details_choice = menu_utils.choose_from_numbered_list(conversations_list, prompt="Please choose a conversation to view details or go back: ")
            if not conversation_details_choice or conversation_details_choice == "Back":
                continue
            conversations_menu.manage_conversation_details_menu(data, conversation_details_choice)

        elif topic_details_choice == "View courses":
            print("You've chosen to view all courses this topic is assigned to.\n")
            if not topic_entry["course_statuses"]:
                print("This topic is not assigned to any course!\n")
                continue
            courses_list = []
            course_labels = []
            for course_code, status in topic_entry["course_statuses"].items():
                for course in data["courses"]:
                    if course["code"].lower() == course_code.lower():
                        course_labels.append(f'{course_code} - {course["name"]} - status: {status}')
                        courses_list.append(course)
            print("\n==================================================================================")
            print("Current list of courses for this topic:")
            print("==================================================================================\n")
            menu_utils.print_numbered_list(course_labels)
            courses_list.extend(["Back"])
            course_details_choice = menu_utils.choose_from_numbered_list(courses_list, prompt="Please choose a course to view details or go back: ")
            if not course_details_choice or course_details_choice == "Back":
                continue
            courses_menu.manage_course_details_menu(data, course_details_choice)

        elif topic_details_choice == "Delete topic":
            confirmation = input("Please confirm you would like to delete this topic: Y/N? ").strip().lower()
            if confirmation == "y":
                deleted, reason = topics.delete_topic(data, topic_entry["name"])
                if deleted:
                    print("Topic deleted!\n")
                    break
                elif reason == "topic has conversations":
                    print("This topic has conversations associated, not possible to delete!\n")
            else:
                print("Topic is not deleted!\n")

        elif topic_details_choice == "Back":
            break 