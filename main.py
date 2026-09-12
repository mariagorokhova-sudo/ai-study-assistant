import topics

data = topics.load_data()

while True:
    print("\nAI Study Assistant")
    print("1. List topics")
    print("2. Add topic")
    print("3. Delete topic")
    print("4. Exit")

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
        print("Goodbye!")
        break
    else:
        print("Invalid option!")
    