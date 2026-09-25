import conversations

def test_create_conversation():
    data = {"topics": [],  "conversations": []}
    topic = "recursion"
    ai_mode = "socratic tutor"

    result = conversations.create_conversation(data, topic, ai_mode)

    assert data == {
        "topics": [], 
         
        "conversations": [
            {
            "topic": "recursion", 
            "ai_mode": "socratic tutor", 
            "messages": []
            }
        ]
    }

    assert result == {
            "topic": "recursion", 
            "ai_mode": "socratic tutor", 
            "messages": []
            }

def test_add_message_to_existing_conversation():
    data = {
        "topics": [], 
         
        "conversations": [
            {
            "topic": "recursion", 
            "ai_mode": "socratic tutor", 
            "messages": []
            }
        ]
    }
    role = "user"
    content = "What is recursion?"

    conversations.add_message_to_conversation(data["conversations"][0], role, content)

    assert data == {
        "topics": [], 
         
        "conversations": [
            {
            "topic": "recursion", 
            "ai_mode": "socratic tutor", 
            "messages": [
                {"role": "user",
                "content": "What is recursion?"}]
            }
        ]
    }

def test_add_second_message_to_conversation():
    data = {
        "topics": [], 
         
        "conversations": [
            {
            "topic": "recursion", 
            "ai_mode": "socratic tutor", 
            "messages": [
                {"role": "user",
                "content": "What is recursion?"}]
            }
        ]
    }

    role = "assistant"
    content = "**Recursion** is when a function calls itself to solve a smaller version of the same problem."

    conversations.add_message_to_conversation(data["conversations"][0], role, content)

    assert data == {
        "topics": [], 
         
        "conversations": [
            {
            "topic": "recursion", 
            "ai_mode": "socratic tutor", 
            "messages": [
                {"role": "user",
                "content": "What is recursion?"},
                {"role": "assistant",
                "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
            }
        ]
    }

def test_get_conversations_by_topic():
    data = {
        "topics": [], 
         
        "conversations": [
            {
            "topic": "recursion", 
            "ai_mode": "socratic tutor", 
            "messages": [
                {"role": "user",
                "content": "What is recursion?"},
                {"role": "assistant",
                "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
            },
            {
            "topic": "recursion", 
            "ai_mode": "Debugger", 
            "messages": [
                {"role": "user",
                "content": "Question on debugging?"},
                {"role": "assistant",
                "content": "Answer on debugging"}]
            },
            {
                "topic": "classes", 
                "ai_mode": "socratic tutor", 
                "messages": [
                    {"role": "user",
                    "content": "What is inheritance"},
                    {"role": "assistant",
                    "content": "Inheritance lets one class reuse another class."}]
            }
        ]
    }

    topic_name = "recursion"

    result = conversations.get_conversations_by_topic(data, topic_name)

    assert result == [{
        "topic": "recursion", 
        "ai_mode": "socratic tutor", 
        "messages": [
            {"role": "user",
            "content": "What is recursion?"},
            {"role": "assistant",
            "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
        },
        {
        "topic": "recursion", 
        "ai_mode": "Debugger", 
        "messages": [
            {"role": "user",
            "content": "Question on debugging?"},
            {"role": "assistant",
            "content": "Answer on debugging"}]
        }]

def test_get_last_user_message():
    conversation_entry = {
        "topic": "recursion", 
        "ai_mode": "socratic tutor", 
        "messages": [
            {"role": "user",
            "content": "What is base case?"},
            {"role": "assistant",
            "content": "Base case is ..."},
            {"role": "user",
            "content": "What is recursion?"},
            {"role": "assistant",
            "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
        }

    last_user_message = conversations.get_last_user_message(conversation_entry)

    assert last_user_message == "What is recursion?"

def test_get_unique_conversations_topics():
    data = {
        "topics": [], 
         
        "conversations": [
            {
            "topic": "Recursion", 
            "ai_mode": "socratic tutor", 
            "messages": [
                {"role": "user",
                "content": "What is recursion?"},
                {"role": "assistant",
                "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
            },
            {
            "topic": "recursion", 
            "ai_mode": "Debugger", 
            "messages": [
                {"role": "user",
                "content": "Question on debugging?"},
                {"role": "assistant",
                "content": "Answer on debugging"}]
            },
            {
                "topic": "classes", 
                "ai_mode": "socratic tutor", 
                "messages": [
                    {"role": "user",
                    "content": "What is inheritance"},
                    {"role": "assistant",
                    "content": "Inheritance lets one class reuse another class."}]
            }
        ]
    }

    conversation_topics_list = conversations.get_unique_conversations_topics(data)

    assert conversation_topics_list == ["Recursion", "classes"]

def test_count_conversations_by_topic():
    data = {
        "topics": [], 
         
        "conversations": [
            {
            "topic": "recursion", 
            "ai_mode": "socratic tutor", 
            "messages": [
                {"role": "user",
                "content": "What is recursion?"},
                {"role": "assistant",
                "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
            },
            {
            "topic": "Recursion", 
            "ai_mode": "Debugger", 
            "messages": [
                {"role": "user",
                "content": "Question on debugging?"},
                {"role": "assistant",
                "content": "Answer on debugging"}]
            },
            {
                "topic": "classes", 
                "ai_mode": "socratic tutor", 
                "messages": [
                    {"role": "user",
                    "content": "What is inheritance"},
                    {"role": "assistant",
                    "content": "Inheritance lets one class reuse another class."}]
            }
        ]
    }

    result = conversations.count_conversations_by_topic(data)

    assert result == {"recursion": 2, "classes": 1}

def test_sorting_conversation_counts_descending():
    counts = {
        "classes": 1,
        "recursion": 2,
        "algorithms": 2
    }

    result = conversations.sort_conversations_counts_descending(counts)

    assert result == [
        ("algorithms", 2),
        ("recursion", 2),
        ("classes", 1)
    ]





