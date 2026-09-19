import topics
import ai
import openai
import history
import topics_menu
import history_menu
import ai_menu

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
            topics_menu.manage_topics_menu(data)

        elif choice == "2":
            ai_menu.manage_ai_menu(data)

        elif choice == "3":
            history_menu.manage_history_menu(data)
 
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
        