def print_numbered_topics(topic_names_list):
    for number, topic_name in enumerate(topic_names_list, start=1):
        print(f"{number}. {topic_name}")
    print("\n")

def print_numbered_topics_with_other_option(topic_names_list):
    for number, topic_name in enumerate(topic_names_list, start=1):
        print(f"{number}. {topic_name}")
    last_option = len(topic_names_list)+1
    print(f"{last_option}. Other\n")

def choose_topic_from_enumerated_list(topic_names_list):
    if not topic_names_list:
        print("No topics yet!\n")
        return
    try:
        topic_choice = int(input("Please enter a topic number: "))
    except ValueError:
        print("Invalid option!\n")
        return
  
    if topic_choice > len(topic_names_list) or topic_choice < 1:
        print("Invalid option!\n")
        return
    else:
        return topic_names_list[topic_choice - 1]

def choose_topic_from_enumerated_list_with_other_option(topic_names_list):
    if not topic_names_list:
        print("No topics yet!\n")
        return
    last_option = len(topic_names_list)+1
    try:
        topic_choice = int(input("Please enter a topic number: "))
    except ValueError:
        print("Invalid option!\n")
        return
  
    if topic_choice > last_option or topic_choice < 1:
        print("Invalid option!\n")
        return
    elif topic_choice == last_option:
        topic_name = input("Please enter a topic name: ")
        if not topic_name:
            print("Topic name cannot be empty!\n")
            return
        return topic_name
    else:
        return topic_names_list[topic_choice - 1]

def print_numbered_topics_with_details(data):
    print("\nCurrent list of topics with details:\n")
    for number, topic_details in enumerate(data["topics"], start=1):
        print(f'{number}. {topic_details["name"]}')
        print(f'Status: {topic_details["status"]}')
        if not topic_details["notes"]:
            print("Notes: no notes yet!\n")
        else:
            print(f'Notes:')
            for note in topic_details["notes"]:
                print(f'- {note}')
            print("\n")

def print_history_entries(entries_list):
    if not entries_list:
        print("No history on this topic yet!\n")
    else:
        for entry in entries_list:
            print(f"\nTopic: {entry['topic']}")
            print(f"Question: {entry['question']}")
            print(f"Answer: {entry['answer']}")


