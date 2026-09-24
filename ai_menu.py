import ai
import openai
import topics
import storage
import menu_utils
import conversations

def manage_ai_menu(data):
    topics_list = topics.list_topics(data)
    menu_utils.print_numbered_list_with_last_option(topics_list)
    topic_name = menu_utils.choose_from_enumerated_list_with_last_option(topics_list)
    if topic_name is None:
        return
    if topic_name == "new":
        topic_name = input("Please enter a topic name: ").strip()
        if not topic_name:
            print("Topic name cannot be empty!\n")
            return

    conversations_list = conversations.get_conversations_by_topic(data, topic_name)
    menu_utils.print_numbered_conversations(conversations_list)
    conversation_entry = menu_utils.choose_from_enumerated_list_with_last_option(conversations_list)

    if conversation_entry is None:
        return

    elif conversation_entry == "new":
        ai_modes_list = ["Tutor", "Socratic tutor", "Debugger", "Code reviewer", "Examiner"]
        print("\nPlease choose AI mode:")
        menu_utils.print_numbered_list(ai_modes_list)
        ai_mode = menu_utils.choose_topic_from_enumerated_list(ai_modes_list)
        if not ai_mode:
            return

    while True:
        question = input("Please enter your question or /exit: ")
        if question == "/exit":
            break
        
        if conversation_entry == "new":
            conversation_entry = conversations.create_conversation(data, topic_name, ai_mode)

        conversations.add_message_to_conversation(conversation_entry, "user", question)
        
        try:
            answer = ai.ask_about_topic(conversation_entry)
            print(f"\n{answer}")
            conversations.add_message_to_conversation(conversation_entry, "assistant", answer)
        except openai.APIError:
            print("Sorry, the AI request failed. Please try again.")
        storage.save_topics(data)

    
    
