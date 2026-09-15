import history
from unittest.mock import patch

def test_add_history_entry():
    with patch("history.storage.save_topics") as mock_save:

        data = {
            "topics": [
                {
                    "name": "recursion",
                    "status": "new",
                    "notes": ""
                }
            ],
            "history": []
        }

        topic = "recursion"
        question = "what is a base case?"
        answer = "A **base case** tells a recursive function when to stop calling itself. Without one, the function would keep calling itself forever, eventually causing an error."
        

        history.add_history_entry(data, topic, question, answer)

        assert data["history"][0] == {
            "topic": topic,
            "question": question,
            "answer": answer
        }

        mock_save.assert_called_once_with(data)

def test_add_history_entry_to_exisiting_history():
    with patch("history.storage.save_topics"):
        data = {
            "topics": [
                {
                    "name": "recursion",
                    "status": "new",
                    "notes": ""
                }
            ],
            "history": [
                {
                    "topic": "classes",
                    "question": "what is inheritance?",
                    "answer": "Inheritance allows a class to inherit from another class."
                }
            ]
        }

        old_entry = data["history"][0].copy()

        topic = "recursion"
        question = "what is a base case?"
        answer = "A **base case** tells a recursive function when to stop calling itself. Without one, the function would keep calling itself forever, eventually causing an error."
        
        history.add_history_entry(data, topic, question, answer)

        assert len(data["history"]) == 2
        assert data["history"][0] == old_entry
        assert data["history"][1] == {
            "topic": topic,
            "question": question,
            "answer": answer
        }

def test_list_history_entries():
    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": ""
            }
        ],
        "history": [
            {
                "topic": "classes",
                "question": "what is inheritance?",
                "answer": "Inheritance allows a class to inherit from another class."
            },
            {
                "topic": "recursion",
                "question": "what is a base case?",
                "answer": "A **base case** tells a recursive function when to stop calling itself. Without one, the function would keep calling itself forever, eventually causing an error."
            }
        ]
    }

    entries = history.list_history_entries(data)

    assert entries == data["history"]

def test_list_history_entries_when_empty():
    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": ""
            }
        ],
        "history": []
    }

    entries = history.list_history_entries(data)

    assert entries == []

def test_get_history_by_topic():

    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": ""
            }
        ],
        "history": [
            {
                "topic": "classes",
                "question": "what is inheritance?",
                "answer": "Inheritance allows a class to inherit from another class."
            },
            {
                "topic": "recursion",
                "question": "what is a base case?",
                "answer": "A **base case** tells a recursive function when to stop calling itself."
            },
            {
                "topic": "recursion",
                "question": "why do we need a base case?",
                "answer": "Without one, the function would keep calling itself forever, eventually causing an error."
            }
        ]
    }

    result = history.get_history_by_topic(data, "recursion")

    assert result == [
            {
                "topic": "recursion",
                "question": "what is a base case?",
                "answer": "A **base case** tells a recursive function when to stop calling itself."
            },
            {
                "topic": "recursion",
                "question": "why do we need a base case?",
                "answer": "Without one, the function would keep calling itself forever, eventually causing an error."
            }
    ]

def test_get_history_no_such_topic():
    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": ""
            }
        ],
        "history": [
            {
                "topic": "classes",
                "question": "what is inheritance?",
                "answer": "Inheritance allows a class to inherit from another class."
            }
        ]
    }

    result = history.get_history_by_topic(data, "recursion")

    assert result == []



