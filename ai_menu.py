import ai
import openai
import topics
import storage
import menu_utils
import conversations

def manage_ai_menu(data):
    topics_list = topics.list_topics(data)
    print("\n==================================================================================")
    print("Current list of topics:")
    print("==================================================================================\n")
    menu_utils.print_numbered_list(topics_list, include_other_option=True)
    topic_name = menu_utils.choose_from_numbered_list(topics_list, include_other_option=True, prompt="Please choose a topic to discuss with AI: ")
    if topic_name is None:
        return
    if topic_name == "new":
        print("You've chosen 'Other' option.")
        topic_name = input("Please enter a topic name: ").strip()
        if not topic_name:
            print("Topic name cannot be empty!\n")
            return
        topics.add_topic(data, topic_name)
    print(f"\nYou've chosen {topic_name}.")

    conversations_list = conversations.get_conversations_by_topic(data, topic_name)
    menu_utils.print_numbered_conversations(conversations_list)
    conversation_entry = menu_utils.choose_from_numbered_list(conversations_list, include_other_option=True, prompt="Please choose an option to continue or start a new conversation: ")

    if conversation_entry is None:
        return

    elif conversation_entry == "new":
        print("You've chosen to start new conversation.")
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
        
        if conversation_entry == "new":
            conversation_entry = conversations.create_conversation(data, topic_name, ai_mode)

        conversations.add_message_to_conversation(conversation_entry, "user", question)
        
        try:
            answer = ai.ask_about_topic(conversation_entry)
            print("\n-----------------------------------------------------------------------------------")
            print(f"\n{answer}")
            conversations.add_message_to_conversation(conversation_entry, "assistant", answer)
        except openai.APIError as error:
            conversation_entry["messages"].pop()
            print("Sorry, the AI request failed. Please try again.")
            print(error)
        storage.save_topics(data)

    
    
