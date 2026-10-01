import topics
from unittest.mock import patch
import pytest

def test_add_topic():
    data = {"topics": []}

    with patch("topics.storage.save_data") as mock_save:
        added, reason = topics.add_topic(data, "recursion")

        assert added is True
        assert reason == "added"
        assert data["topics"] == [
            {
                "name": "recursion",
                "status": "new",
                "notes": []
            }
        ]
        mock_save.assert_called_once_with(data)


def test_add_duplicate_topic():
    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": ""
            }
        ]
    }

    with patch("topics.storage.save_data") as mock_save:
        added, reason = topics.add_topic(data, "recursion")

        assert added is False
        assert reason == "duplicate"
        assert data == {
                    "topics": [
                        {
                            "name": "recursion",
                            "status": "new",
                            "notes": ""
                        }
                    ]
                }
        mock_save.assert_not_called()


def test_add_duplicate_topic_different_case():
    data = {
        "topics": [
            {
                "name": "classes",
                "status": "new",
                "notes": ""
            }
        ]
    }

    with patch("topics.storage.save_data") as mock_save:
        added, reason = topics.add_topic(data, "Classes")

        assert added is False
        assert reason == "duplicate"
        assert data == {
                    "topics": [
                        {
                            "name": "classes",
                            "status": "new",
                            "notes": ""
                        }
                    ]
                }
        mock_save.assert_not_called()


def test_add_empty_topic():
    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": ""
            }
        ]
    }

    with patch("topics.storage.save_data") as mock_save:
        added, reason = topics.add_topic(data, "   ")

        assert added is False
        assert reason == "empty"
        assert data == {
            "topics": [
                {
                    "name": "recursion",
                    "status": "new",
                    "notes": ""
                }
            ]
        }

        mock_save.assert_not_called()


def test_delete_topic():
    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": ""
            },
            {
                "name": "git",
                "status": "new",
                "notes": ""
            }
        ]
    }

    with patch("topics.storage.save_data") as mock_save:
        deleted, reason = topics.delete_topic(data, "Recursion")

        assert deleted is True
        assert reason == "deleted"
        assert data == {
            "topics": [
                {
                    "name": "git",
                    "status": "new",
                    "notes": ""
                }
            ]
        }
        mock_save.assert_called_once_with(data)


def test_delete_topic_not_found():
    data = {
        "topics": [
            {
                "name": "git",
                "status": "new",
                "notes": ""
            }
        ]
    }

    with patch("topics.storage.save_data") as mock_save:
        deleted, reason = topics.delete_topic(data, "recursion")

        assert deleted is False
        assert reason == "not found"
        assert data == {
            "topics": [
                {
                    "name": "git",
                    "status": "new",
                    "notes": ""
                }
            ]
        }
        mock_save.assert_not_called()


def test_delete_empty_topic():
    data = {
        "topics": [
            {
                "name": "git",
                "status": "new",
                "notes": ""
            }
        ]
    }

    with patch("topics.storage.save_data") as mock_save:
        deleted, reason = topics.delete_topic(data, "  ")

        assert deleted is False
        assert reason == "empty"
        assert data == {
            "topics": [
                {
                    "name": "git",
                    "status": "new",
                    "notes": ""
                }
            ]
        }

        mock_save.assert_not_called()


def test_change_topic_status():
    with patch("topics.storage.save_data") as mock_save:
        data = {
            "topics": [
                {
                    "name": "recursion",
                    "status": "new",
                    "notes": []
                }
            ]
        }

        topic_name = "Recursion"
        new_status = " In Progress "

        topics.change_topic_status(data, topic_name, new_status)

        assert data["topics"] == [
            {
                "name": "recursion",
                "status": "in progress",
                "notes": []
            }
        ]
       
        mock_save.assert_called_once_with(data)


@pytest.mark.parametrize(
    "topic_name, new_status, reason", 
    [("recursion", "banana", "invalid status"), 
    ("graphs", "in progress", "topic not found")])
def test_change_topic_status_invalid_input(topic_name, new_status, reason):
    with patch("topics.storage.save_data") as mock_save:
        data = {
            "topics": [
                {
                    "name": "recursion",
                    "status": "new",
                    "notes": ""
                }
            ]
        }

        result, actual_reason = topics.change_topic_status(data, topic_name, new_status)

        assert result == False
        assert actual_reason == reason
        assert data["topics"] == [
            {
                "name": "recursion",
                "status": "new",
                "notes": ""
            }
        ]
        mock_save.assert_not_called()


def test_add_note_to_existing_notes():
    with patch("topics.storage.save_data") as mock_save:
        data = {
                "topics": [
                    {
                        "name": "recursion",
                        "status": "new",
                        "notes": ["Base case stops recursion"]
                    }
                ]
            }
        topic_name = "recursion"
        new_note = "Recursive case calls the function again"

        result, reason = topics.add_note(data, topic_name, new_note)

        assert result == True
        assert reason == "added"
        assert data["topics"] == [
                    {
                        "name": "recursion",
                        "status": "new",
                        "notes": ["Base case stops recursion",
                                "Recursive case calls the function again"]
                    }
                ]
        mock_save.assert_called_once_with(data)


@pytest.mark.parametrize("topic_name, new_note, reason", 
                        [("functions", "note about function", "topic not found"),
                        ("recursion", "", "empty note"),
                        (("recursion", "  ", "empty note"))])
def test_add_note_to_existing_notes_invalid_input(topic_name, new_note, reason):
    with patch("topics.storage.save_data") as mock_save:
        data = {
            "topics": [
                {
                    "name": "recursion",
                    "status": "new",
                    "notes": ["Base case stops recursion"]
                }
            ]
        }
        result, actual_reason = topics.add_note(data, topic_name, new_note)

        assert result == False
        assert actual_reason == reason
        assert data["topics"] == [
            {
                "name": "recursion",
                "status": "new",
                "notes": ["Base case stops recursion"]
            }
        ]
        mock_save.assert_not_called()


def test_topics_get_notes_for_existing_topic():
    data = {
        "topics": [
            {"name": "Recursion",
            "status": "in progress",
            "notes": [
                "Recursion is when a function calls itself.",
                "You need a base case so that a function knows where to stop"
            ]}
        ],
        "conversations": []
    }
    result = topics.get_notes(data, "recursion")

    assert result == [
            "Recursion is when a function calls itself.",
            "You need a base case so that a function knows where to stop"
            ]


def test_topics_get_notes_for_existing_topic_empty_notes():
    data = {
        "topics": [
            {
                "name": "Recursion",
                "status": "in progress",
                "notes": []
            }
        ],
        "conversations": []
    }

    result = topics.get_notes(data, "recursion")

    assert result == []


def test_topics_get_notes_for_nonexisting_topic():
    data = {
        "topics": [
            {"name": "Recursion",
            "status": "in progress",
            "notes": [
                "Recursion is when a function calls itself.",
                "You need a base case so that a function knows where to stop"
            ]}
        ],
        "conversations": []
    }
    result = topics.get_notes(data, "classes")

    assert result is None


def test_delete_note():
    data = {
        "topics": [
            {
                "name": "Recursion",
                "status": "in progress",
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("topics.storage.save_data") as mock_save:
        result, reason = topics.delete_note(data, "Recursion", 0)

        assert data == {
            "topics": [
                {
                    "name": "Recursion",
                    "status": "in progress",
                    "notes": ["recursive case"]
                }
            ],
            "conversations": []
        }
        mock_save.assert_called_once_with(data)
        assert result == True
        assert reason == "deleted"


@pytest.mark.parametrize("incorrect_index", [2, -1])
def test_delete_note_incorrect_index(incorrect_index):
    data = {
        "topics": [
            {
                "name": "Recursion",
                "status": "in progress",
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("topics.storage.save_data") as mock_save:
        result, reason = topics.delete_note(data, "Recursion", incorrect_index)

        assert data == {
            "topics": [
                {
                    "name": "Recursion",
                    "status": "in progress",
                    "notes": ["base case", "recursive case"]
                }
            ],
            "conversations": []
        }
        mock_save.assert_not_called()
        assert result == False
        assert reason == "incorrect index"


def test_delete_note_topic_not_found():
    data = {
        "topics": [
            {
                "name": "Recursion",
                "status": "in progress",
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("topics.storage.save_data") as mock_save:
        result, reason = topics.delete_note(data, "Classes", 0)

        assert data == {
            "topics": [
                {
                    "name": "Recursion",
                    "status": "in progress",
                    "notes": ["base case", "recursive case"]
                }
            ],
            "conversations": []
        }
        mock_save.assert_not_called()
        assert result is False
        assert reason == "topic not found"