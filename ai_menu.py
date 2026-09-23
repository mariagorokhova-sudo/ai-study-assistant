import ai
import openai
import topics
import history
import storage
import menu_utils
import conversations

def manage_ai_menu(data):
    menu_utils.print_numbered_topics_with_other_option(topics.list_topics(data))
    topic_name = menu_utils.choose_topic_from_enumerated_list_with_other_option(topics.list_topics(data))
    if not topic_name:
        return

    ai_modes_list = ["Tutor", "Socratic tutor", "Debugger", "Code reviewer", "Examiner"]
    print("\nPlease choose AI mode:")
    menu_utils.print_numbered_topics(ai_modes_list)
    ai_mode = menu_utils.choose_topic_from_enumerated_list(ai_modes_list)
    if not ai_mode:
        return

    conversation_entry = conversations.create_conversation(data, topic_name, ai_mode)

    question = input("Please enter your question: ")
    conversations.add_message_to_conversation(conversation_entry, "user", question)
    

    previous_history = history.get_history_by_topic(data, topic_name)
    try:
        answer = ai.ask_about_topic(topic_name, question, previous_history)
        print(f"\n{answer}")
        conversations.add_message_to_conversation(conversation_entry, "assistant", answer)
    except openai.APIError:
        print("Sorry, the AI request failed. Please try again.")
    storage.save_topics(data)
    
