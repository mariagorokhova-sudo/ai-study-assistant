import main
from unittest.mock import patch
import openai
import httpx
import history
import pytest

def test_ai_api_error():
    with patch("builtins.input") as mock_input:
        with patch("main.ai.ask_about_topic") as mock_ask:
            with patch("main.history.add_history_entry") as mock_history:
                with patch("builtins.print") as mock_print:
                    with patch("main.topics.list_topics") as mock_list_topics:
                        mock_list_topics.return_value = ["recursion", "classes", "algorythms"]
                        mock_input.side_effect = [
                            "2",
                            "1",
                            "what is recursion?",
                            "4"
                        ]

                        request = httpx.Request("POST", "https://api.openai.com/v1/responses")
                        mock_ask.side_effect = openai.APIConnectionError(request=request)

                        main.main()

                        mock_print.assert_any_call("Sorry, the AI request failed. Please try again.")
                        mock_history.assert_not_called()

def test_ai_request_success_add_to_history():
    with patch("builtins.input") as mock_input:
        with patch("main.ai.ask_about_topic") as mock_ask:
            with patch("main.history.add_history_entry") as mock_history:
                with patch("main.history.get_history_by_topic") as mock_get_history:
                    with patch("main.topics.list_topics") as mock_list_topics:
                        mock_list_topics.return_value = ["recursion", "classes", "algorythms"]
                        
                        mock_input.side_effect = [
                                        "2",
                                        "2",
                                        "what is inheritance?",
                                        "4"
                                    ]
                        
                        mock_get_history.return_value = [
                            {
                                "topic": "classes",
                                "question": "what is a class?",
                                "answer": "A class is ..."
                            }
                        ]
                        mock_ask.return_value = "Inheritance allows a class to inherit from another class."

                        main.main()

                        mock_get_history.assert_called_once_with(main.data, "classes")
                        mock_ask.assert_called_once_with("classes", "what is inheritance?", mock_get_history.return_value)
                        mock_history.assert_called_once_with(
                            main.data,
                            "classes",
                            "what is inheritance?",
                            "Inheritance allows a class to inherit from another class."
                        )

def test_invalid_topic_input():
    with patch("builtins.input", side_effect = ["2", "abc", "4"]):
        with patch("main.ai.ask_about_topic") as mock_ask:
            with patch("main.topics.list_topics") as mock_list_topics:
                with patch("builtins.print") as mock_print:
                    mock_list_topics.return_value = ["recursion", "classes", "algorythms"]

                    main.main()

                    mock_print.assert_any_call("Invalid option!")
                    mock_ask.assert_not_called()

def test_other_topic_option():
    with patch("main.topics.list_topics") as mock_list_topics:
        with patch("builtins.input") as mock_input:
            with patch("main.ai.ask_about_topic") as mock_ask:
                with patch("main.history.get_history_by_topic") as mock_history_by_topic:
                    with patch("main.history.add_history_entry") as mock_history:
                        mock_list_topics.return_value = ["recursion", "classes", "algorythms"]
                        mock_input.side_effect = [
                            "2",
                            "4",
                            "binary trees",
                            "what is a binary tree?",
                            "4"
                        ]
                        mock_history_by_topic.return_value = []

                        mock_ask.return_value == "A binary tree is a ..."

                        main.main()

                        mock_ask.assert_called_once_with(
                            "binary trees",
                            "what is a binary tree?", 
                            mock_history_by_topic.return_value)

@pytest.mark.parametrize("edge_choice", ["0", "99"])
def test_invalid_topic_input_edge_cases(edge_choice):
    with patch("builtins.input", side_effect = ["2", edge_choice, "4"]):
        with patch("main.ai.ask_about_topic") as mock_ask:
            with patch("main.topics.list_topics") as mock_list_topics:
                with patch("builtins.print") as mock_print:
                    with patch("main.history.add_history_entry") as mock_history:
                        mock_list_topics.return_value = ["recursion", "classes", "algorythms"]

                        main.main()

                        mock_print.assert_any_call("Invalid option!")
                        mock_ask.assert_not_called()
                        mock_history.assert_not_called()

def test_manage_topics_add_to_main_menu():
    with patch("builtins.input", side_effect = ["1", "6", "4"]):
        with patch("builtins.print") as mock_print:

            main.main()

            mock_print.assert_any_call("4. Change topic status")
            mock_print.assert_any_call("5. Add new note")















            







            

