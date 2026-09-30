import storage
import conversations
import pytest
import json

def test_save_topics(tmp_path, monkeypatch):
    test_file = tmp_path/"test_topics.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": []
            }
        ],
        "conversations": []
    }

    storage.save_topics(data)

    assert test_file.exists()
    
    loaded_data = storage.load_topics()
    assert loaded_data == data

def test_load_topics_when_file_does_not_exist(tmp_path, monkeypatch):
    test_file = tmp_path/"missing.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    loaded_data = storage.load_topics()

    assert loaded_data == {"topics": [], "conversations": []}

@pytest.mark.parametrize("data",
                         [
                            {"topics": "", "conversations":[]},
                            {"topics": [], "conversations": ""},
                            [],
                            {"topics": ["recursion"], "conversations": []},
                            {
                                "topics": [
                                    {
                                        "status": "new",
                                        "notes": []
                                    }
                                ],
                                "conversations": []
                            },
                            {
                                "topics": [
                                    {
                                        "name": 123,
                                        "status": "new",
                                        "notes": []
                                    }
                                ],
                                "conversations": []
                            },
                            {
                                "topics": [
                                    {
                                        "name": "Recursion",
                                        "status": 123,
                                        "notes": ["A note"]
                                    }
                                ],
                                "conversations": []
                            },
                            {
                                "topics": [
                                    {
                                        "name": "Recursion",
                                        "status": "new",
                                        "notes": "A note"
                                    }
                                ],
                                "conversations": []
                            },
                            {
                                "topics": [
                                    {
                                        "name": "Recursion",
                                        "status": "new",
                                        "notes": ["A note", 123]
                                    }
                                ],
                                "conversations": []
                            },
                            {
                                "topics": [],
                                "conversations": ["broken conversation"]
                            },
                            {
                                "topics": [],
                                "conversations": [
                                    {
                                        "topic": "Recursion",
                                        "ai_mode": "Tutor"
                                    }
                                ]
                            },
                            {
                                "topics": [],
                                "conversations": [
                                    {
                                        "topic": 123,
                                        "ai_mode": "Tutor",
                                        "messages": []
                                    }
                                ]
                            },
                            {
                                "topics": [],
                                "conversations": [
                                    {
                                        "topic": "Recursion",
                                        "ai_mode": 123,
                                        "messages": []
                                    }
                                ]
                            },
                            {
                                "topics": [],
                                "conversations": [
                                    {
                                        "topic": "Recursion",
                                        "ai_mode": "Tutor",
                                        "messages": "Not a list"
                                    }
                                ]
                            },
                            {
                                "topics": [],
                                "conversations": [
                                    {
                                        "topic": "Recursion",
                                        "ai_mode": "Tutor",
                                        "messages": ["Broken message"]
                                    }
                                ]
                            },
                            {
                                "topics": [],
                                "conversations": [
                                    {
                                        "topic": "Recursion",
                                        "ai_mode": "Tutor",
                                        "messages": [{}]
                                    }
                                ]
                            },
                            {
                                "topics": [],
                                "conversations": [
                                    {
                                        "topic": "Recursion",
                                        "ai_mode": "Tutor",
                                        "messages": [
                                            {
                                                "role": 123,
                                                "content": "What is recursion?"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "topics": [],
                                "conversations": [
                                    {
                                        "topic": "Recursion",
                                        "ai_mode": "Tutor",
                                        "messages": [
                                            {
                                                "role": "user",
                                                "content": 123
                                            }
                                        ]
                                    }
                                ]
                            }
                         ])
def test_load_topics_invalid_structure(tmp_path, monkeypatch, data):
    test_file = tmp_path/"test_topics.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    with test_file.open("w") as file:
        json.dump(data, file)

    with pytest.raises(ValueError):
        storage.load_topics()



def test_save_new_conversation(tmp_path, monkeypatch):
    test_file = tmp_path/"test_conversations.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    data = {"topics": [], "conversations": []}
    topic = "recursion"
    ai_mode = "socratic tutor"

    conversation_entry = conversations.create_conversation(data, topic, ai_mode)
    
    role = "user"
    content = "What is recursion?"

    conversations.add_message_to_conversation(conversation_entry, role, content)
    storage.save_topics(data)

    assert test_file.exists()
    
    loaded_data = storage.load_topics()

    assert loaded_data == {
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

def test_damaged_json_file(tmp_path, monkeypatch):
    test_file = tmp_path/"test_file.json"
    invalid_json = '{"topics": ['
    with test_file.open("w") as file:
        file.write(invalid_json)
    monkeypatch.setattr(storage, "DATA_FILE", test_file)
    with pytest.raises(ValueError, match="Invalid JSON file"):
        storage.load_topics()











