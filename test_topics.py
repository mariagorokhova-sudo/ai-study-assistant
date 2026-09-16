import topics
from unittest.mock import patch

def test_add_topic():
    data = {"topics": []}

    with patch("topics.storage.save_topics") as mock_save:
        added, reason = topics.add_topic(data, "recursion")

        assert added is True
        assert reason == "added"
        assert data["topics"] == [
            {
                "name": "recursion",
                "status": "new",
                "notes": ""
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

    with patch("topics.storage.save_topics") as mock_save:
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

    with patch("topics.storage.save_topics") as mock_save:
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

    with patch("topics.storage.save_topics") as mock_save:
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

    with patch("topics.storage.save_topics") as mock_save:
        deleted, reason = topics.delete_topic(data, "recursion")

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

    with patch("topics.storage.save_topics") as mock_save:
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

    with patch("topics.storage.save_topics") as mock_save:
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

def test_get_topics_not_discussed_with_ai():
    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": ""
            },
            {
                "name": "classes",
                "status": "new",
                "notes": ""
            },
            {
                "name": "algorithms",
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

    topics_not_discussed_with_ai = topics.get_topics_not_discussed_with_ai(data)

    assert topics_not_discussed_with_ai == {"algorithms"}




