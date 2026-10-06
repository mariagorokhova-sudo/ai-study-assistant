import main
from unittest.mock import patch

def test_manage_courses_add_to_main_menu():
    data = {"topics": [], "conversations": []}
    with patch("builtins.input", side_effect = ["1", "5"]):
        with patch("main.courses_menu.manage_courses_menu") as mock_courses_menu:
            with patch("main.topics.load_data", return_value=data):

                main.main()

                mock_courses_menu.assert_called_once_with(data)


def test_manage_topics_add_to_main_menu():
    data = {"topics": [], "conversations": []}
    with patch("builtins.input", side_effect = ["2", "5"]):
        with patch("main.topics_menu.manage_topics_menu") as mock_topics_menu:
            with patch("main.topics.load_data", return_value=data):

                main.main()

                mock_topics_menu.assert_called_once_with(data)


def test_manage_ai_add_to_main_menu():
    data = {"topics": [], "conversations": []}
    with patch("builtins.input", side_effect = ["3", "5"]):
        with patch("main.ai_menu.manage_ai_menu") as mock_ai_menu:
            with patch("main.topics.load_data", return_value=data):

                main.main()

                mock_ai_menu.assert_called_once_with(data)


def test_manage_conversations_add_to_main_menu():
    data = {"topics": [], "conversations": []}
    with patch("builtins.input", side_effect = ["4", "5"]):
        with patch("main.conversations_menu.manage_conversations_menu") as mock_conversations_menu:
            with patch("main.topics.load_data", return_value=data):

                main.main()

                mock_conversations_menu.assert_called_once_with(data)


def test_main_json_file_damaged():
    with patch("main.topics.load_data") as mock_load:
        with patch("builtins.print") as mock_print:
            mock_load.side_effect = ValueError("Invalid JSON file")

            main.main()

            mock_print.assert_any_call("JSON file is corrupted and cannot be read.")