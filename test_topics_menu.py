import topics_menu
import topics
from unittest.mock import patch
import pytest

def test_delete_topic_option_wrong_choice():
    data = {
        "topics":[
            {
                "name": "recursion",
                "status": "new",
                "notes": []
            }
        ]
    }
    with patch("builtins.input", side_effect=["3", "6"]):
        with patch("topics_menu.menu_utils.choose_topic_from_enumerated_list") as mock_choice:
            with patch("topics_menu.topics.delete_topic") as mock_delete:
                mock_choice.return_value = None
                
                topics_menu.manage_topics_menu(data)

                mock_delete.assert_not_called()

def test_delete_topic_option_success():
    data = {
        "topics":[
            {
                "name": "recursion",
                "status": "new",
                "notes": []
            }
        ]
    }
    with patch("builtins.input", side_effect=["3", "6"]):
        with patch("topics_menu.menu_utils.choose_topic_from_enumerated_list") as mock_choice:
            with patch("menu_utils.print_numbered_topics") as mock_print_numbered_topics:
                with patch("topics_menu.topics.delete_topic") as mock_delete:
                    with patch("builtins.print") as mock_print:
                        mock_choice.return_value = "recursion"
                        mock_delete.return_value = True, "deleted"
                        topics_menu.manage_topics_menu(data)

                        mock_delete.assert_called_once_with(data, "recursion")
                        mock_print.assert_any_call("Topic deleted!")
                        assert mock_print_numbered_topics.call_count == 2

def test_change_topic_status_success():
    data = {
        "topics":[
            {
                "name": "recursion",
                "status": "new",
                "notes": []
            }
        ]
    }
    with patch("builtins.input", side_effect = ["4", "in progress", "6"]):
        with patch("topics_menu.topics.change_topic_status") as mock_change_status:
            with patch("topics_menu.menu_utils.choose_topic_from_enumerated_list") as mock_choice:
                with patch("builtins.print") as mock_print:
                    with patch("menu_utils.print_numbered_topics_with_details") as mock_print_numbered_topics:
                        mock_choice.return_value = "recursion"
                        mock_change_status.return_value = (True, "changed")

                        topics_menu.manage_topics_menu(data)

                        mock_change_status.assert_called_once_with(data, "recursion", "in progress")
                        mock_print.assert_any_call("Status changed!")
                        mock_print_numbered_topics.assert_called_once_with(data)
                        

def test_change_topic_status_unsuccessful():
    data = {
        "topics":[
            {
                "name": "recursion",
                "status": "new",
                "notes": []
            }
        ]
    }
    with patch("builtins.input", side_effect = ["4", "in progress", "6"]):
        with patch("topics_menu.topics.change_topic_status") as mock_change_status:
            with patch("topics_menu.menu_utils.choose_topic_from_enumerated_list") as mock_choice:
                with patch("builtins.print") as mock_print:
                    mock_choice.return_value = "recursion"
                    mock_change_status.return_value = (False, "invalid status")

                    topics_menu.manage_topics_menu(data)

                    mock_change_status.assert_called_once_with(data, "recursion", "in progress")
                    mock_print.assert_any_call("Invalid status!\n")

def test_topics_menu_add_new_note():
    data = {
        "topics":[
            {
                "name": "recursion",
                "status": "new",
                "notes": []
            },
            {
                "name": "binary tress",
                "status": "in progress",
                "notes": ["Binary tree is a..."]
            }
        ]
    }
    with patch("builtins.input", side_effect = ["5", "Tree has a root node", "6"]):
        with patch("menu_utils.choose_topic_from_enumerated_list") as mock_choice:
            with patch("topics_menu.topics.add_note") as mock_add_note:
                mock_choice.return_value = "binary trees"
                mock_add_note.return_value = (True, "added")

                topics_menu.manage_topics_menu(data)

                mock_add_note.assert_called_once_with(data, "binary trees", "Tree has a root node")

def test_topics_menu_add_new_note_empty_list():
    data = {"topics":[], "history": []}
    with patch("builtins.input", side_effect = ["5", "6"]):
        with patch("menu_utils.choose_topic_from_enumerated_list") as mock_choice:
            with patch("topics_menu.topics.add_note") as mock_add_note:
                mock_choice.return_value = None

                topics_menu.manage_topics_menu(data)

                mock_add_note.assert_not_called()

def test_topic_menu_get_topics_with_details():
    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "in progress",
                "notes": ["note 1", "note 2"]
            },
            {
                "name": "classes",
                "status": "new",
                "notes": []
            }
        ],
        "history": []
    }
    with patch("builtins.input", side_effect = ["1", "6"]):
        with patch("topics_menu.menu_utils.print_numbered_topics_with_details") as mock_print_numbered_topics:

            topics_menu.manage_topics_menu(data)

            mock_print_numbered_topics.assert_called_once_with(data)

            


