import main
from unittest.mock import patch

def test_manage_topics_add_to_main_menu():
    with patch("builtins.input", side_effect = ["1", "4"]):
        with patch("main.topics_menu.manage_topics_menu") as mock_topics_menu:

            main.main()

            mock_topics_menu.assert_called_once_with(main.data)















            







            

