import history
import menu_utils

def manage_history_menu(data):
    while True:
        print("\n1. View all history")
        print("2. View history on specific topic")
        print("3. View question counts by topic")
        print("4. Back")

        choice_history = input("Please choose an option: ").strip()

        if choice_history == "1":
            print("\nCurrent list of history topics with details:")
            entries_list = history.list_history_entries(data)
            menu_utils.print_history_entries(entries_list)

        elif choice_history == "2":
            history_topic_list = sorted(history.get_unique_history_topics(data))
            if not history_topic_list:
                print("No history yet!\n")
                continue
            print("\nCurrent list of history topics:")
            menu_utils.print_numbered_list(history_topic_list)
            topic_name = menu_utils.choose_topic_from_enumerated_list(history_topic_list)
            if not topic_name:
                continue
            entries_list = history.get_history_by_topic(data, topic_name)
            menu_utils.print_history_entries(entries_list)

        elif choice_history == "3":
            topic_counts = history.count_history_by_topics(data)
            if not topic_counts:
                print("No history yet!\n")
                continue
            counts_sorted = history.sort_topics_counts_descending(topic_counts)
            print("\nHistory topics by counts descending:\n")
            for topic, count in counts_sorted:
                print(f"{topic}: {count}")
        
        elif choice_history == "4":
            break

        else:
            print("Invalid option!\n")
            continue
