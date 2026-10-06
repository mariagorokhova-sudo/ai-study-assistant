import storage
import conversations
from unittest.mock import patch
import pytest
import json

def test_save_data(tmp_path, monkeypatch):
    test_file = tmp_path / "test_data.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    data = {
        "courses": [],
        "topics": [
            {
                "name": "recursion",
                "course_statuses": {},
                "notes": []
            }
        ],
        "conversations": []
    }

    storage.save_data(data)

    assert test_file.exists()
    
    loaded_data = storage.load_data()
    assert loaded_data == data


def test_load_data_when_file_does_not_exist(tmp_path, monkeypatch):
    test_file = tmp_path / "missing.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    loaded_data = storage.load_data()

    assert loaded_data == {"courses": [], "topics": [], "conversations": []}

@pytest.mark.parametrize("data",
                         [
                            {"courses": "", "topics": [], "conversations": []},
                            {"courses": [], "topics": "", "conversations":[]},
                            {"courses": [], "topics": [], "conversations": ""},
                            [],
                            {"courses": ["Data structures"], "topics": [], "conversations": []},
                            {"courses": [
                                {
                                    "code": "XX1035-01",
                                    "session": "October - March 2027",
                                    "status": "active"
                                }
                            ],
                            "topics": [],
                            "conversations": []},
                            {"courses": [
                                {
                                    "code": 123,
                                    "name": "Algorithms and Data Structures I",
                                    "session": "October - March 2027",
                                    "status": "active"
                                }
                            ],
                            "topics": [],
                            "conversations": []},
                            {"courses": [
                                {
                                    "code": "XX1035-01",
                                    "name": 123,
                                    "session": "October - March 2027",
                                    "status": "active"
                                }
                            ],
                            "topics": [],
                            "conversations": []},
                            {"courses": [
                                {
                                    "code": "XX1035-01",
                                    "name": "Algorithms and Data Structures",
                                    "session": 123,
                                    "status": "active"
                                }
                            ],
                            "topics": [],
                            "conversations": []},
                            {"courses": [
                                {
                                    "code": "XX1035-01",
                                    "name": "Algorithms and Data Structures",
                                    "session": "October - March 2027",
                                    "status": 123
                                }
                            ],
                            "topics": [],
                            "conversations": []},
                            {"courses": [], "topics": ["recursion"], "conversations": []},
                            {
                                "courses": [],
                                "topics": [
                                    {
                                        "course_statuses": {},
                                        "notes": []
                                    }
                                ],
                                "conversations": []
                            },
                            {
                                "topics": [
                                    {
                                        "name": 123,
                                        "course_statuses": {},
                                        "notes": []
                                    }
                                ],
                                "conversations": []
                            },
                            {
                                "topics": [
                                    {
                                        "name": "Recursion",
                                        "course_statuses": [],
                                        "notes": ["A note"]
                                    }
                                ],
                                "conversations": []
                            },
                            {
                                "topics": [
                                    {
                                        "name": "Recursion",
                                        "course_statuses": {"XX1035-01": 123},
                                        "notes": ["A note"]
                                    }
                                ],
                                "conversations": []
                            },
                            {
                                "topics": [
                                    {
                                        "name": "Recursion",
                                        "course_statuses": {},
                                        "notes": "A note"
                                    }
                                ],
                                "conversations": []
                            },
                            {
                                "topics": [
                                    {
                                        "name": "Recursion",
                                        "course_statuses": {},
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
def test_load_data_invalid_structure(tmp_path, monkeypatch, data):
    test_file = tmp_path / "test_data.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    with test_file.open("w") as file:
        json.dump(data, file)

    with pytest.raises(ValueError):
        storage.load_data()


def test_save_new_conversation(tmp_path, monkeypatch):
    test_file = tmp_path / "test_conversations.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    data = {"courses": [], "topics": [], "conversations": []}
    topic = "recursion"
    ai_mode = "socratic tutor"

    conversation_entry = conversations.create_conversation(data, topic, ai_mode)
    
    role = "user"
    content = "What is recursion?"

    conversations.add_message_to_conversation(conversation_entry, role, content)
    storage.save_data(data)

    assert test_file.exists()
    
    loaded_data = storage.load_data()

    assert loaded_data == {
        "courses": [],
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
    test_file = tmp_path / "test_file.json"
    invalid_json = '{"topics": ['
    with test_file.open("w") as file:
        file.write(invalid_json)
    monkeypatch.setattr(storage, "DATA_FILE", test_file)
    with pytest.raises(ValueError, match="Invalid JSON file"):
        storage.load_data()


def test_save_data_preserves_existing_file_on_error(tmp_path, monkeypatch):
    test_file = tmp_path / "test_data.json"
    original_content = '{"topics": [], "conversations": []}'
    test_file.write_text(original_content)
    monkeypatch.setattr(storage, "DATA_FILE", test_file)
    temporary_file = test_file.with_suffix(".tmp")
    with patch("storage.json.dump", side_effect=TypeError("Data is not JSON serializable")):
        with pytest.raises(TypeError):
            storage.save_data({"topics": [], "conversations": []})

        assert test_file.read_text() == original_content
        assert not temporary_file.exists()


def test_data_file_location_is_independent_of_working_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    assert storage.DATA_FILE.exists()


def test_add_courses_to_old_json(tmp_path, monkeypatch):
    test_file = tmp_path / "test_data.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    data = {"topics": [], "conversations": []}
    with test_file.open("w") as file:
        json.dump(data, file)

    assert test_file.exists()
    
    loaded_data = storage.load_data()
    assert loaded_data == {"courses": [], "topics": [], "conversations": []}
    assert list(loaded_data.keys()) == ["courses", "topics", "conversations"]


def test_load_data_not_affect_existing_courses(tmp_path, monkeypatch):
    test_file = tmp_path / "test_data.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            }
        ],
        "topics": [],
        "conversations": []
    }
    storage.save_data(data)
    loaded_data = storage.load_data()

    assert loaded_data == data