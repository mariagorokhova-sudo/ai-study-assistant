import topics_menu
import topics
from unittest.mock import patch
import pytest

def test_delete_topic_option_wrong_choice():
    data = {
        "topics":[
            {
                "name": "recursion",
                "course_statuses": {},
                "notes": []
            }
        ]
    }
    with patch("builtins.input", side_effect=["3", "2", "6"]):
        with patch("topics_menu.topics.delete_topic") as mock_delete:

            topics_menu.manage_topics_menu(data)

            mock_delete.assert_not_called()


def test_delete_topic_option_success():
    data = {
        "topics":[
            {
                "name": "recursion",
                "course_statuses": {},
                "notes": []
            }
        ]
    }
    with patch("builtins.input", side_effect=["3", "1", "y", "6"]):
        with patch("menu_utils.print_numbered_list") as mock_print_numbered_topics:
            with patch("topics_menu.topics.delete_topic") as mock_delete:
                with patch("builtins.print") as mock_print:
                    mock_delete.return_value = True, "deleted"
                    topics_menu.manage_topics_menu(data)

                    mock_delete.assert_called_once_with(data, "recursion")
                    mock_print.assert_any_call("Topic deleted!")


def test_delete_topic_option_unsuccess_has_conversations():
    data = {
        "topics":[
            {
                "name": "recursion",
                "course_statuses": {},
                "notes": []
            }
        ],
        "conversations": [
            {
                "topic": "recursion",
                "ai_mode": "Tutor",
                "messages": [
                    {
                        "role": "user",
                        "content": "what is recursion?"
                    }
                ]
            }
        ]
    }
    with patch("builtins.input", side_effect=["3", "1", "y", "6"]):
        with patch("menu_utils.print_numbered_list") as mock_print_numbered_topics:
            with patch("topics_menu.topics.delete_topic") as mock_delete:
                with patch("builtins.print") as mock_print:
                    mock_delete.return_value = False, "topic has conversations"
                    topics_menu.manage_topics_menu(data)

                    mock_delete.assert_called_once_with(data, "recursion")
                    mock_print.assert_any_call("This topic has conversations associated, not possible to delete!\n")


def test_topics_menu_add_new_note():
    data = {
        "topics":[
            {
                "name": "recursion",
                "course_statuses": {},
                "notes": []
            },
            {
                "name": "binary trees",
                "course_statuses": {},
                "notes": ["Binary tree is a..."]
            }
        ]
    }
    with patch("builtins.input", side_effect = ["4", "2", "Tree has a root node", "6"]):
        with patch("topics_menu.topics.add_note") as mock_add_note:
            mock_add_note.return_value = (True, "added")

            topics_menu.manage_topics_menu(data)

            mock_add_note.assert_called_once_with(data, "binary trees", "Tree has a root node")


def test_topics_menu_add_new_note_empty_list():
    data = {"topics":[], "conversations": []}
    with patch("builtins.input", side_effect = ["4", "6"]):
        with patch("topics_menu.topics.add_note") as mock_add_note:

            topics_menu.manage_topics_menu(data)

            mock_add_note.assert_not_called()


def test_topics_menu_get_topics_with_details():
    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "in progress",
                "notes": ["note 1", "note 2"]
            },
            {
                "name": "classes",
                "course_statuses": {},
                "notes": []
            }
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect = ["1", "6"]):
        with patch("topics_menu.menu_utils.print_numbered_topics_with_details") as mock_print_numbered_topics:

            topics_menu.manage_topics_menu(data)

            mock_print_numbered_topics.assert_called_once_with(data)


def test_topics_menu_delete_note_success():
    data = {
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {},
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect=["5", "1", "1", "y", "6"]):
        with patch("topics_menu.topics.delete_note") as mock_delete_note:
            mock_delete_note.return_value = (True, "deleted")

            topics_menu.manage_topics_menu(data)

            mock_delete_note.assert_called_once_with(data, "Recursion", 0)


def test_topics_menu_delete_note_empty_notes():
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
    with patch("builtins.input", side_effect=["5", "1", "6"]):
        with patch("topics_menu.topics.delete_note") as mock_delete_note:
            with patch("builtins.print") as mock_print:

                topics_menu.manage_topics_menu(data)

                mock_delete_note.assert_not_called()
                mock_print.assert_any_call("No notes for this topic yet!\n")


def test_topics_menu_delete_note_incorrect_index():
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
    with patch("builtins.input", side_effect=["5", "1", "3", "6"]):
        with patch("topics_menu.topics.delete_note") as mock_delete_note:

            topics_menu.manage_topics_menu(data)

            mock_delete_note.assert_not_called()