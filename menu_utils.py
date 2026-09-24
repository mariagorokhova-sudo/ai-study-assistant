import conversations

def print_numbered_list(options_list):
    for number, option in enumerate(options_list, start=1):
        print(f"{number}. {option}")
    print("\n")

def print_numbered_list_with_last_option(options_list):
    for number, option in enumerate(options_list, start=1):
        print(f"{number}. {option}")
    last_option = len(options_list)+1
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

def print_numbered_conversations(conversations_list):
    if not conversations_list:
        print("No conversations on this topic yet!")
        print("1. Start new conversation\n")
        return
    else:
        last_option = len(conversations_list)+1
        print("List of previous conversations:")
        for number, conversation in enumerate(conversations_list, start=1):
            last_user_message = conversations.get_last_user_message(conversation)
            print(f'{number}. AI mode: {conversation["ai_mode"]} | Last question: {last_user_message}')
        print("========== or you can ========")
        print(f'{last_option}. Start new conversation\n')  

def choose_from_enumerated_list_with_last_option(options_list):
    last_option = len(options_list)+1
    try:    
        user_choice = int(input("Please choose an option: ")) 
    except ValueError:
        print("Invalid option!\n")
        return
    if user_choice > last_option or user_choice < 1:
        print("Invalid option!\n")
        return
    elif user_choice == last_option:
        return "new"
    else:
        return options_list[user_choice-1]



