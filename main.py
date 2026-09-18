import topics
import ai
import openai
import history

data = topics.load_data()

def main():
    while True:
        print("\nAI Study Assistant")
        print("1. Manage topics")
        print("2. Ask AI")
        print("3. View history")
        print("4. Exit")

        choice = input("Please choose an option: ").strip()

        if choice == "1":
            while True:
                print("1. List topics")
                print("2. Add topic")
                print("3. Delete topic")
                print("4. Change topic status")
                print("5. Add new note")
                print("6. Back")

                manage_choice = input("Please choose an option: ").strip()

                if manage_choice == "1":
                    if not data["topics"]:
                        print("No topics yet!")
                    else:
                        for number, topic_details in enumerate(data["topics"], start=1):
                            print(f'{number}. {topic_details["name"]}')
                            print(f'Status: {topic_details["status"]}')
                            if not topic_details["notes"]:
                                print("Notes: no notes yet!")
                            else:
                                print(f'Notes:')
                                for note in topic_details["notes"]:
                                    print(f'- {note}')


                elif manage_choice == "2":
                    name = input("Please enter a topic name: ")
                    added, reason = topics.add_topic(data, name)
            
                    if added:
                        print("Topic added!")
                    elif reason == "empty":
                        print("Topic could not be empty!")
                    elif reason == "duplicate":
                        print("Topic already exists!")

                elif manage_choice == "3":
                    name = input("Please enter a topic name: ")
                    deleted, reason = topics.delete_topic(data, name)

                    if deleted:
                        print("Topic deleted!")
                    elif reason == "empty":
                        print("Topic could not be empty!")
                    elif reason == "not found":
                        print("Topic not found!")

                elif manage_choice == "4":
                    topic_name = input("Please enter a topic name: ")
                    print("Available statuses are: new, in progress, exam prep, finished.")
                    new_status = input("Please enter new status for your topic: ")
                    changed, reason = topics.change_topic_status(data, topic_name, new_status)
                    if changed:
                        print("Status changed!")
                    elif reason == "invalid status":
                        print("Invalid status!")
                    elif reason == "topic not found":
                        print("Topic not found!")

                elif manage_choice == "5":
                    topic_names = topics.list_topics(data)
                    if not topic_names:
                        print("No topics yet!")
                        continue
                    for i in range (1, len(topic_names)+1):
                        print(f"{i}. {topic_names[i-1]}.")
                    
                    try:
                        topic_choice = int(input("Please enter a topic number: "))
                    except ValueError:
                        print("Invalid option!")
                        continue
                    
                    if topic_choice > len(topic_names) or topic_choice < 1:
                        print("Invalid option!")
                        continue
                    else:
                        topic = topic_names[topic_choice - 1]

                    new_note = input("Please enter your note: ")

                    added, reason = topics.add_note(data, topic, new_note)
                    if added:
                        print("Note added!")
                    elif reason == "empty note":
                        print("It's not possible to add an empty note!")

                elif manage_choice == "6":
                    break

                else:
                    print("Invalid option!")

        elif choice == "2":
            topic_names = topics.list_topics(data)
            for i in range (1, len(topic_names)+1):
                print(f"{i}. {topic_names[i-1]}.")
            last_option = len(topic_names)+1
            print(f"{last_option}. Other.")
            try:
                topic_choice = int(input("Please enter a topic number: "))
            except ValueError:
                print("Invalid option!")
                continue
            
            if topic_choice > last_option or topic_choice < 1:
                print("Invalid option!")
                continue
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

        elif choice == "3":
            print("\n1. View all history")
            print("2. View history on specific topic")
            print("3. View question counts by topic")

            choice_history = input("Please choose an option: ").strip()
            if choice_history == "1":
                entries_list = history.list_history_entries(data)
                
            elif choice_history == "2":
                topic = input("Please enter a topic name: ")
                entries_list = history.get_history_by_topic(data, topic)

            elif choice_history == "3":
                topic_counts = history.count_history_by_topics(data)
                counts_sorted = history.sort_topics_counts_descending(topic_counts)
                for topic, count in counts_sorted:
                    print(f"{topic}: {count}")
                continue
            
            else:
                print("Invalid option!")
                continue

            if not entries_list:
                    print("No history yet!")
            else:
                for entry in entries_list:
                    print(f"\nTopic: {entry['topic']}")
                    print(f"Question: {entry['question']}")
                    print(f"Answer: {entry['answer']}")
 
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
        