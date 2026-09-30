import main
from unittest.mock import patch

def test_manage_topics_add_to_main_menu():
    data = {"topics": [], "conversations": []}
    with patch("builtins.input", side_effect = ["1", "4"]):
        with patch("main.topics_menu.manage_topics_menu") as mock_topics_menu:
            with patch("main.topics.load_data", return_value=data):

                main.main()

                mock_topics_menu.assert_called_once_with(data)


def test_main_json_file_damaged():
    with patch("main.topics.load_data") as mock_load:
        with patch("builtins.print") as mock_print:
            mock_load.side_effect = ValueError("Invalid JSON file")

            main.main()

            mock_print.assert_any_call("JSON file is corrupted and cannot be read.")