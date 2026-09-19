import ai
import openai
import topics
import history

def manage_ai_menu(data):
    topic_names = topics.list_topics(data)
    for number, topic_name in enumerate(topic_names, start=1):
        print(f"{number}. {topic_name}.")
    last_option = len(topic_names)+1
    print(f"{last_option}. Other.")
    try:
        topic_choice = int(input("Please enter a topic number: "))
    except ValueError:
        print("Invalid option!")
        return
    
    if topic_choice > last_option or topic_choice < 1:
        print("Invalid option!")
        return
    elif topic_choice == last_option:
        topic = input("Please enter a topic name: ")
    else:
        topic = topic_names[topic_choice - 1]
    
    question = input("Please enter your question: ")
    previous_history = history.get_history_by_topic(data, topic)

    try:
        answer = ai.ask_about_topic(topic, question, previous_history)
        print(f"\n{answer}")
        history.add_history_entry(data, topic, question, answer)
    except openai.APIError:
        print("Sorry, the AI request failed. Please try again.")
