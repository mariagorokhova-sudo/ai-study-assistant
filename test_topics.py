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


