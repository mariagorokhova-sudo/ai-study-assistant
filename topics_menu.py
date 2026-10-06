import topics
import menu_utils

def manage_topics_menu(data):
    
    if not data["topics"]:
        print("No topics yet!")
    else:
        print("\n===========================")
        print("Current list of topics:")
        print("===========================\n")
        menu_utils.print_numbered_list(topics.list_topics(data))
    
    while True:
        topics_options = [
            "List topics with details",
            "Add topic",
            "Delete topic",
            "Change topic status",
            "Add new note",
            "Delete note",
            "Back"
        ]
        print("===================================================================================")
        menu_utils.print_numbered_list(topics_options)
        topics_choice = menu_utils.choose_from_numbered_list(topics_options)
        print("===================================================================================\n")

        if topics_choice == "List topics with details":
            if not data["topics"]:
                print("No topics yet!")
            else:
                menu_utils.print_numbered_topics_with_details(data)

        elif topics_choice == "Add topic":
            print("You've chosen to add topic.")
            topic_name = input("Please enter a topic name: ")
            print(f"\nYou've entered: {topic_name}")
            added, reason = topics.add_topic(data, topic_name)
    
            if added:
                print("Topic added!")
                print("\n==================================================================================")
                print("Updated list of topics:")
                print("==================================================================================\n")
                menu_utils.print_numbered_list(topics.list_topics(data))
            elif reason == "empty":
                print("Topic could not be empty!\n")
            elif reason == "duplicate":
                print("Topic already exists!\n")

        elif topics_choice == "Delete topic":
            if not data["topics"]:
                print("No topics yet!")
                continue
            else:
                print("You've chosen to delete topic.")
                print("\n===========================")
                print("Current list of topics:")
                print("===========================\n")
                menu_utils.print_numbered_list(topics.list_topics(data))
            topic_name = menu_utils.choose_from_numbered_list(topics.list_topics(data), prompt="Please choose a topic to delete: ")
            if not topic_name:
                continue
            print(f"\nYou've chosen: {topic_name}")
            confirmation = input("Please confirm you would like to delete this topic: Y/N?").strip().lower()
            if confirmation == "y":
                deleted, reason = topics.delete_topic(data, topic_name)
                if deleted:
                    print("Topic deleted!")
                    print("\n===================================================================================")
                    print("Updated list of topics:")
                    print("===================================================================================\n")
                    menu_utils.print_numbered_list(topics.list_topics(data))
            else:
                print("Topic is not deleted!\n")
                continue

        elif topics_choice == "Change topic status":
            print("You've chosen to change topic status.")
            print("\n===========================")
            print("Current list of topics:")
            print("===========================\n")
            menu_utils.print_numbered_list(topics.list_topics(data))
            topic_name = menu_utils.choose_from_numbered_list(topics.list_topics(data), prompt="Please choose a topic to change status: ")
            if not topic_name:
                continue
            print(f"You've chosen: {topic_name}")
            print("Available statuses are: new, in progress, exam prep, finished.")
            new_status = input("Please enter new status for your topic: ")
            changed, reason = topics.change_topic_status(data, topic_name, new_status)
            if changed:
                print("Status changed!")
                menu_utils.print_numbered_topics_with_details(data)
            elif reason == "invalid status":
                print("Invalid status!\n")

        elif topics_choice == "Add new note":
            print("You've chosen to add a note to the topic.")
            print("\n==================================================================================")
            print("Current list of topics:")
            print("==================================================================================\n")
            menu_utils.print_numbered_list(topics.list_topics(data))
            topic_name = menu_utils.choose_from_numbered_list(topics.list_topics(data), prompt="Please choose a topic to add note: ")
            if not topic_name:
                continue
            print(f"You've chosen: {topic_name}")
            new_note = input("Please enter your note: ")
            added, reason = topics.add_note(data, topic_name, new_note)
            if added:
                print("Note added!\n")
                menu_utils.print_numbered_topics_with_details(data)
            elif reason == "empty note":
                print("It's not possible to add an empty note!\n")

        elif topics_choice == "Delete note":
            print("You've chosen to delete a note from the topic.")
            print("\n==================================================================================")
            print("Current list of topics:")
            print("==================================================================================\n")
            menu_utils.print_numbered_list(topics.list_topics(data))
            topic_name = menu_utils.choose_from_numbered_list(topics.list_topics(data), prompt="Please choose a topic to delete a note: ")
            if not topic_name:
                continue
            print(f"You've chosen: {topic_name}")
            print("\n==================================================================================")
            print(f'Current list of notes for {topic_name}:')
            print("==================================================================================\n")
            notes_list = topics.get_notes(data, topic_name)
            if not notes_list:
                print("No notes for this topic yet!\n")
                continue
            menu_utils.print_numbered_list(notes_list)
            note_index = menu_utils.choose_from_numbered_list(notes_list,
                                                              prompt="Please choose a note to delete: ",
                                                              return_index=True)
            if note_index is None:
                continue
            confirmation = input("Please confirm you would like to delete this note: Y/N?").strip().lower()
            if confirmation == "y":
                deleted, reason = topics.delete_note(data, topic_name, note_index)
                if deleted:
                    print("Note deleted!\n")
                    menu_utils.print_numbered_topics_with_details(data)
                elif reason == "incorrect index":
                    print("Impossible to delete, note index is incorrect.\n")
            else:
                print("Note is not deleted!\n")
                continue

        elif topics_choice == "Back":
            break