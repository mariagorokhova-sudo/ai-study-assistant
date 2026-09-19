import history

def manage_history_menu(data):
    print("\n1. View all history")
    print("2. View history on specific topic")
    print("3. View question counts by topic")

    choice_history = input("Please choose an option: ").strip()

    if choice_history == "1":
        entries_list = history.list_history_entries(data)

    elif choice_history == "2":
        topic = input("Please enter a topic name: ")
        entries_list = history.get_history_by_topic(data, topic)

    elif choice_history == "3":
        topic_counts = history.count_history_by_topics(data)
        counts_sorted = history.sort_topics_counts_descending(topic_counts)
        for topic, count in counts_sorted:
            print(f"{topic}: {count}")
        return

    else:
        print("Invalid option!")
        return

    if not entries_list:
            print("No history yet!")
    else:
        for entry in entries_list:
            print(f"\nTopic: {entry['topic']}")
            print(f"Question: {entry['question']}")
            print(f"Answer: {entry['answer']}")