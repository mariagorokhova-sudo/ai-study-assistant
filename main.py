import topics
import ai
import openai
import history

data = topics.load_data()

def main():
    while True:
        print("\nAI Study Assistant")
        print("1. List topics")
        print("2. Add topic")
        print("3. Delete topic")
        print("4. Ask AI")
        print("5. View history")
        print("6. Exit")

        choice = input("Please choose an option: ").strip()

        if choice == "1":
            topic_names = topics.list_topics(data)
            if not topic_names:
                print("No topics yet!")
            else:
                for name in topic_names:
                    print(name)

        elif choice == "2":
            name = input("Please enter a topic name: ")
            added, reason = topics.add_topic(data, name)
            
            if added:
                print("Topic added!")
            elif reason == "empty":
                print("Topic could not be empty!")
            elif reason == "duplicate":
                print("Topic already exists!")
        
        elif choice == "3":
            name = input("Please enter a topic name: ")
            deleted, reason = topics.delete_topic(data, name)

            if deleted:
                print("Topic deleted!")
            elif reason == "empty":
                print("Topic could not be empty!")
            elif reason == "not found":
                print("Topic not found!")

        elif choice == "4":
            topic = input("Please enter your topic: ")
            question = input("Please enter your question: ")

            try:
                answer = ai.ask_about_topic(topic, question)
                print(answer)
                history.add_history_entry(data, topic, question, answer)
            except openai.APIError:
                print("Sorry, the AI request failed. Please try again.")

        elif choice == "5":
            entries_list = history.list_history_entries(data)
            if not entries_list:
                print("No history yet!")
            else:
                for entry in entries_list:
                    print(f"Topic: {entry['topic']}")
                    print(f"Question: {entry['question']}")
                    print(f"Answer: {entry['answer']}")
            
        
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
        