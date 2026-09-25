import json
import topics
import topics_menu
import conversations_menu
import ai_menu

def main():
    try:
        data = topics.load_data()
    except json.JSONDecodeError:
        print("JSON file is corrupted and cannot be read.")
        return
    while True:
        print("\nAI Study Assistant")
        print("1. Manage topics")
        print("2. Ask AI")
        print("3. View conversation history")
        print("4. Exit")

        choice = input("Please choose an option: ").strip()

        if choice == "1":
            topics_menu.manage_topics_menu(data)

        elif choice == "2":
            ai_menu.manage_ai_menu(data)

        elif choice == "3":
            conversations_menu.manage_conversations_menu(data)
 
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
        