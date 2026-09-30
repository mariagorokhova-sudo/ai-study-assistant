import topics
import topics_menu
import conversations_menu
import ai_menu

def main():
    try:
        data = topics.load_data()
    except ValueError:
        print("JSON file is corrupted and cannot be read.")
        return
    while True:
        print("\n============================")
        print("AI Study Assistant")
        print("============================\n")
        print("1. Manage topics")
        print("2. Ask AI")
        print("3. View conversation history")
        print("4. Exit\n")
        print("============================\n")

        choice = input("Please choose an option from the list above: ").strip()

        if choice == "1":
            print("You've chosen to manage topics.")
            topics_menu.manage_topics_menu(data)

        elif choice == "2":
            print("You've chosen to ask AI assistant.")
            ai_menu.manage_ai_menu(data)

        elif choice == "3":
            print("You've chosen to view conversation history.")
            conversations_menu.manage_conversations_menu(data)
 
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()