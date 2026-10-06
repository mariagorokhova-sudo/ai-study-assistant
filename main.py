import topics
import courses_menu
import topics_menu
import conversations_menu
import ai_menu
import menu_utils

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
        main_menu_options = [
            "Manage courses",
            "Manage topics",
            "Ask AI",
            "View conversation history",
            "Exit"
        ]
        menu_utils.print_numbered_list(main_menu_options)
        choice = menu_utils.choose_from_numbered_list(main_menu_options, prompt="Please choose a menu option: ")
        print("\n============================\n")

        if choice == "Manage courses":
            print("You've chosen to manage courses.")
            courses_menu.manage_courses_menu(data)

        elif choice == "Manage topics":
            print("You've chosen to manage topics.")
            topics_menu.manage_topics_menu(data)

        elif choice == "Ask AI":
            print("You've chosen to ask AI assistant.")
            ai_menu.manage_ai_menu(data)

        elif choice == "View conversation history":
            print("You've chosen to view conversation history.")
            conversations_menu.manage_conversations_menu(data)
 
        elif choice == "Exit":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()