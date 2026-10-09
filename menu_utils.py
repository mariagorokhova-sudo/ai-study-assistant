import conversations

def print_numbered_list(options_list, include_other_option=False, separator=False):
    for number, option in enumerate(options_list, start=1):
        print(f"{number}. {option}")
        if separator:
            print("...................................................................................")
    if include_other_option:
        last_option = len(options_list)+1
        print(f"{last_option}. Other\n")
    else:
        print("\n")


def choose_from_numbered_list(options_list, include_other_option=False, prompt="Please choose an option from the list above: ", return_index=False):
    if not options_list and not include_other_option:
        print("No options yet!\n")
        return
    last_option = len(options_list)
    if include_other_option:
        last_option+=1
    try:    
        user_choice = int(input(prompt)) 
    except ValueError:
        print("Invalid option!\n")
        return
    if user_choice > last_option or user_choice < 1:
        print("Invalid option!\n")
        return
    elif include_other_option and user_choice == last_option:
        return "new"
    else:
        if return_index:
            return user_choice - 1
        return options_list[user_choice-1]


def print_numbered_topics(data, include_back_option=False):
    print("\n===================================================================================")
    print("Current list of topics")
    print("===================================================================================\n")
    for number, topic_details in enumerate(data["topics"], start=1):
        print(f'{number}. {topic_details["name"]}\n')
        if not topic_details["course_statuses"]:
            print("Topic is not assigned to any courses.\n")
        else:
            print("Course statuses:")
            for course_code, status in topic_details["course_statuses"].items():
                print(f'- {course_code}: {status}')
            print()
        if not topic_details["notes"]:
            print("Notes: no notes yet!\n")
            print("-----------------------------------------------------------------------------------")

        else:
            print(f'Notes:')
            for note in topic_details["notes"]:
                print(f'- {note[:30]}...')
                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("-----------------------------------------------------------------------------------")
    if include_back_option:
        print(f'{len(data["topics"]) + 1}. Back')
        print()


def print_numbered_conversations(conversations_list, include_new_option=False, include_back_option=False):
    if not conversations_list:
        print("No conversations yet!\n")
        if include_new_option:
            print("1. Start new conversation\n")
            if include_back_option:
                print("2. Back\n")
        else:
            if include_back_option:
                print("1. Back\n")
        return
    print("\n===================================================================================")
    print("Current list of conversations:")
    print("===================================================================================\n")
    for number, conversation in enumerate(conversations_list, start=1):
        last_user_message = conversations.get_last_user_message(conversation)
        print(f'{number}. Topic: {conversation["topic"]} | AI mode: {conversation["ai_mode"]} | Last question: {last_user_message}')
        print("-----------------------------------------------------------------------------------\n")
    if include_new_option:
        print("============================== or you can =========================================\n")
        print(f'{len(conversations_list)+1}. Start new conversation\n')
        if include_back_option:
            print("============================== or you can =========================================\n")
            print(f'{len(conversations_list)+2}. Go back\n')
    elif include_back_option:
        print(f'{len(conversations_list)+1}. Back\n')


def print_all_conversation_messages(conversation_entry):
    print("\n===================================================================================")
    print(f'AI mode: {conversation_entry["ai_mode"]}')
    print("-----------------------------------------------------------------------------------\n")
    for entry in conversation_entry["messages"]:
        print(f'{entry["role"].capitalize()}: {entry["content"]}')
        print("-----------------------------------------------------------------------------------\n")