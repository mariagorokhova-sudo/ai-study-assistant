import topics
import menu_utils

def manage_topics_menu(data):
    
    if not data["topics"]:
        print("No topics yet!")
    else:
        print("\nCurrent list of topics:")
        menu_utils.print_numbered_topics(topics.list_topics(data))
    
    while True:
        print("1. List topics with details")
        print("2. Add topic")
        print("3. Delete topic")
        print("4. Change topic status")
        print("5. Add new note")
        print("6. Back")

        manage_choice = input("Please choose an option: ").strip()

        if manage_choice == "1":
            if not data["topics"]:
                print("No topics yet!")
            else:
                menu_utils.print_numbered_topics_with_details(data)

        elif manage_choice == "2":
            topic_name = input("Please enter a topic name: ")
            print(f"\nYou've entered: {topic_name}")
            added, reason = topics.add_topic(data, topic_name)
    
            if added:
                print("Topic added!")
                print("\nUpdated list of topics:\n")
                menu_utils.print_numbered_topics(topics.list_topics(data))
            elif reason == "empty":
                print("Topic could not be empty!\n")
            elif reason == "duplicate":
                print("Topic already exists!\n")

        elif manage_choice == "3":
            topic_name = menu_utils.choose_topic_from_enumerated_list(topics.list_topics(data))
            if not topic_name:
                continue
            print(f"\nYou've chosen: {topic_name}")
            deleted, reason = topics.delete_topic(data, topic_name)

            if deleted:
                print("Topic deleted!")
                print("\nUpdated list of topics:\n")
                menu_utils.print_numbered_topics(topics.list_topics(data))

        elif manage_choice == "4":
            topic_name = menu_utils.choose_topic_from_enumerated_list(topics.list_topics(data))
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

        elif manage_choice == "5":
            topic_name = menu_utils.choose_topic_from_enumerated_list(topics.list_topics(data))
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

        elif manage_choice == "6":
            break

        else:
            print("Invalid option!\n")

