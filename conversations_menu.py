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
            "View conversation counts by topic",
            "Back"
        ]
        menu_utils.print_numbered_list(conversation_options)
        print("===================================================================================\n")

        conversation_choice = menu_utils.choose_from_numbered_list(conversation_options)

        if conversation_choice == "View all conversations":
            print("You've chosen to view all conversations.\n")
            menu_utils.print_numbered_conversations(data["conversations"], include_back_option=True)
            conversation_options = data["conversations"].copy()
            conversation_options.extend(["Back"])
            conversation_entry_choice = menu_utils.choose_from_numbered_list(conversation_options, prompt="Please choose a conversation to view all messages or go back: ")
            if not conversation_entry_choice or conversation_entry_choice == "Back":
                continue
            else:
                manage_conversation_details_menu(data, conversation_entry_choice)

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

        elif conversation_choice == "Back":
            break


def manage_conversation_details_menu(data, conversation_entry):
    while True:
        last_user_message = conversations.get_last_user_message(conversation_entry)
        print("\n-----------------------------------------------------------------------------------")
        print(f'Topic: {conversation_entry["topic"]} | AI mode: {conversation_entry["ai_mode"]} | Last question: {last_user_message}')
        print("-----------------------------------------------------------------------------------\n")
        conversation_details_options = [
            "View full conversation",
            "Continue conversation",
            "Start new conversation with same topic",
            "Create summary",
            "Delete conversation",
            "Back"
        ]
        menu_utils.print_numbered_list(conversation_details_options)
        conversation_details_choice = menu_utils.choose_from_numbered_list(conversation_details_options, prompt="Please choose an action from the list above: ")
        if not conversation_details_choice:
            continue

        elif conversation_details_choice == "View full conversation":
            print("You've chosen to view full conversation.\n")
            menu_utils.print_all_conversation_messages(conversation_entry)

        elif conversation_details_choice == "Continue conversation":
            print("You've chosen to continue conversation.\n")
            topic_notes = topics.get_notes(data, conversation_entry["topic"])

            while True:
                question = input("Please enter your question or /exit: ").strip()
                if question == "/exit":
                    break
                if not question:
                    print("Question cannot be empty, please try again.")
                    continue

                conversations.add_message_to_conversation(conversation_entry, "user", question)

                try:
                    answer = ai.ask_about_topic(conversation_entry, topic_notes)
                    print("\n-----------------------------------------------------------------------------------")
                    print(f"\n{answer}")
                    conversations.add_message_to_conversation(conversation_entry, "assistant", answer)
                except openai.APIError as error:
                    conversation_entry["messages"].pop()
                    print("Sorry, the AI request failed. Please try again.")
                    print(error)
                except ValueError as error:
                    if str(error) != "OPENAI_API_KEY is missing":
                        raise
                    conversation_entry["messages"].pop()
                    print("OPENAI_API_KEY is missing. Please add it to the .env file.")
                    return
                conversations.save_conversation(data)

        elif conversation_details_choice == "Start new conversation with same topic":
            print(f'You have chosen to start new conversation with the same topic: {conversation_entry["topic"]}.\n')
            topic_notes = topics.get_notes(data, conversation_entry["topic"])
            conversation_new_entry = "new"

            ai_modes_list = ["Tutor", "Socratic tutor", "Debugger", "Code reviewer", "Examiner"]
            print("\n===================")
            print("\nAvailable AI modes:\n")
            print("===================\n")
            menu_utils.print_numbered_list(ai_modes_list)
            ai_mode = menu_utils.choose_from_numbered_list(ai_modes_list, prompt="Please choose AI learning mode: ")
            if not ai_mode:
                return

            while True:
                question = input("Please enter your question or /exit: ").strip()
                if question == "/exit":
                    break
                if not question:
                    print("Question cannot be empty, please try again.")
                    continue

                conversation_is_new = conversation_new_entry == "new"
                if conversation_is_new:
                    conversation_new_entry = conversations.create_conversation(data, conversation_entry["topic"], ai_mode)

                conversations.add_message_to_conversation(conversation_new_entry, "user", question)

                try:
                    answer = ai.ask_about_topic(conversation_new_entry, topic_notes)
                    print("\n-----------------------------------------------------------------------------------")
                    print(f"\n{answer}")
                    conversations.add_message_to_conversation(conversation_new_entry, "assistant", answer)
                except openai.APIError as error:
                    conversation_new_entry["messages"].pop()
                    if conversation_is_new:
                        data["conversations"].remove(conversation_new_entry)
                        conversation_new_entry = "new"
                    print("Sorry, the AI request failed. Please try again.")
                    print(error)
                except ValueError as error:
                    if str(error) != "OPENAI_API_KEY is missing":
                        raise
                    conversation_new_entry["messages"].pop()
                    if conversation_is_new:
                        data["conversations"].remove(conversation_new_entry)
                        conversation_new_entry = "new"
                    print("OPENAI_API_KEY is missing. Please add it to the .env file.")
                    return
                conversations.save_conversation(data)

        elif conversation_details_choice == "Create summary":
            print("You've chosen to summarize this conversation.\n")
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

        elif conversation_details_choice == "Delete conversation":
            print("You've chosen to delete this conversation.")
            conversation_index = data["conversations"].index(conversation_entry)
            confirmation = input("Please confirm you would like to delete this conversation: Y/N? ").strip().lower()
            if confirmation == "y":
                deleted, reason = conversations.delete_conversation(data, conversation_index)
                if deleted:
                    print("Conversation deleted!\n")
                    break
                elif reason == "incorrect index":
                    print("Impossible to delete, conversation index is incorrect.\n")
            else:
                print("Conversation is not deleted!\n")
                continue

        elif conversation_details_choice == "Back":
            break