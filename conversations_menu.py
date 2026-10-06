import menu_utils
import conversations
import ai
import openai
import topics

def manage_conversations_menu(data):
    while True:
        print("\n===================================================================================")
        conversation_options = [
            "View all conversations",
            "View conversations on specific topic",
            "View conversation counts by topic",
            "Summarize a conversation",
            "Delete a conversation",
            "Back"
        ]
        menu_utils.print_numbered_list(conversation_options)
        print("===================================================================================\n")

        conversation_choice = menu_utils.choose_from_numbered_list(conversation_options)

        if conversation_choice == "View all conversations":
            print("You've chosen to view all conversations.\n")
            menu_utils.print_numbered_conversations(data["conversations"], include_new_option=False)

        elif conversation_choice == "View conversations on specific topic":
            print("You've chosen to view all conversations on specific topic.\n")
            conversation_topics_list = conversations.get_unique_conversations_topics(data)
            if not conversation_topics_list:
                print("No conversations yet!\n")
                continue
            print("\n===================================================================================")
            print("Current list of conversation topics:")
            print("===================================================================================\n")
            menu_utils.print_numbered_list(conversation_topics_list)
            topic_name = menu_utils.choose_from_numbered_list(conversation_topics_list, prompt="Please choose a topic to view history on: ")
            if not topic_name:
                continue
            print(f"You've chosen to view all conversations about {topic_name}.")
            conversations_list = conversations.get_conversations_by_topic(data, topic_name)
            menu_utils.print_numbered_conversations(conversations_list, include_new_option=False)
            conversation_entry = menu_utils.choose_from_numbered_list(conversations_list, include_other_option=False, prompt="Please choose a conversation to view all messages in it: ")
            if conversation_entry is None:
                continue
            menu_utils.print_all_conversation_messages(conversation_entry)

        elif conversation_choice == "View conversation counts by topic":
            conversation_counts = conversations.count_conversations_by_topic(data)
            if not conversation_counts:
                print("No conversations yet!\n")
                continue
            counts_sorted = conversations.sort_conversations_counts_descending(conversation_counts)
            print("\n==================================================================================")
            print("Conversation topics by counts descending:")
            print("==================================================================================\n")
            for topic, count in counts_sorted:
                print(f"{topic}: {count}")

        elif conversation_choice == "Summarize a conversation":
            print("You've chosen to summarize a conversation.")
            menu_utils.print_numbered_conversations(data["conversations"], include_new_option=False)
            if not data["conversations"]:
                continue
            conversation_entry = menu_utils.choose_from_numbered_list(data["conversations"],
                                                                      prompt="Please choose a conversation to summarize: ",
                                                                      include_other_option=False)
            if conversation_entry is None:
                continue
            try:
                conversation_summary = ai.summarize_conversation(conversation_entry)
            except openai.APIError as error:
                print("Sorry, the AI request failed. Please try again.")
                print(error)
                continue
            except ValueError as error:
                if str(error) != "OPENAI_API_KEY is missing":
                    raise
                print("OPENAI_API_KEY is missing. Please add it to the .env file.")
                continue
            if conversation_summary is None:
                print("Cannot summarize an empty conversation!\n")
                continue
            added, reason = topics.add_note(data, conversation_entry["topic"], conversation_summary)
            if added:
                print(f"\nThe following summary was created: \n{conversation_summary}\n")
                print("Conversation summary added as a note!")
            elif reason == "topic not found":
                print("Topic not found, cannot add a note!\n")
            elif reason == "empty note":
                print("Summary cannot be empty!\n")

        elif conversation_choice == "Delete a conversation":
            print("You've chosen to delete a conversation.")
            menu_utils.print_numbered_conversations(data["conversations"], include_new_option=False)
            if not data["conversations"]:
                continue
            conversation_index = menu_utils.choose_from_numbered_list(data["conversations"],
                                                                      prompt="Please choose a conversation to delete: ",
                                                                      include_other_option=False,
                                                                      return_index=True)
            if conversation_index is None:
                continue
            confirmation = input("Please confirm you would like to delete this conversation: Y/N?").strip().lower()
            if confirmation == "y":
                deleted, reason = conversations.delete_conversation(data, conversation_index)
                if deleted:
                    print("Conversation deleted!\n")
                    menu_utils.print_numbered_conversations(data["conversations"], include_new_option=False)
                elif reason == "incorrect index":
                    print("Impossible to delete, conversation index is incorrect.\n")
            else:
                print("Conversation is not deleted!\n")
                continue

        elif conversation_choice == "Back":
            break