import menu_utils
import conversations

def manage_conversations_menu(data):
    while True:
        print("\n===================================================================================")
        print("You can choose from the following options:\n")
        print("1. View all conversations")
        print("2. View conversations on specific topic")
        print("3. View conversations counts by topic")
        print("4. Back\n")
        print("===================================================================================\n")

        choice_history = input("Please choose an option: ").strip()

        if choice_history == "1":
            menu_utils.print_numbered_conversations(data["conversations"], include_new_option=False)

        elif choice_history == "2":
            print("You've chosen to view all conversations on specific topic.")
            conversation_topics_list = conversations.get_unique_conversations_topics(data)
            if not conversation_topics_list:
                print("No conversations yet!\n")
                continue
            print("\n===================================================================================")
            print("Current list of conversation topics:")
            print("===================================================================================\n")
            menu_utils.print_numbered_list(conversation_topics_list)
            topic_name = menu_utils.choose_from_numbered_list(conversation_topics_list)
            if not topic_name:
                continue
            print(f"You've chosen to view all conversations about {topic_name}")
            conversations_list = conversations.get_conversations_by_topic(data, topic_name)
            menu_utils.print_numbered_conversations(conversations_list, include_new_option=False)
            print("\nYou can view all messages by choosing a conversation.\n")
            conversation_entry = menu_utils.choose_from_numbered_list(conversations_list, include_other_option=False)
            if conversation_entry is None:
                continue
            menu_utils.print_all_conversation_messages(conversation_entry)

        elif choice_history == "3":
            conversation_counts = conversations.count_conversations_by_topic(data)
            if not conversation_counts:
                print("No conversations yet!\n")
                continue
            counts_sorted = conversations.sort_conversations_counts_descending(conversation_counts)
            print("\n==================================================================================")
            print("Conversations topics by counts descending:")
            print("==================================================================================\n")
            for topic, count in counts_sorted:
                print(f"{topic}: {count}")
        
        elif choice_history == "4":
            break

        else:
            print("Invalid option!\n")
            continue
