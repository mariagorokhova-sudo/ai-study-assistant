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

def test_view_history():
    with patch("builtins.input") as mock_input:
        with patch("main.history.list_history_entries") as mock_list_history:
            with patch("builtins.print") as mock_print:
                mock_list_history.return_value = [
                    {
                        "topic": "classes",
                        "question": "what is inheritance?",
                        "answer": "Inheritance allows a class to inherit from another class."
                    }
                ]
                mock_input.side_effect = ["3", "1", "4"]

                main.main()

                mock_print.assert_any_call("\nTopic: classes")
                mock_print.assert_any_call("Question: what is inheritance?")
                mock_print.assert_any_call("Answer: Inheritance allows a class to inherit from another class.")

def test_view_empty_history():
    with patch("builtins.input") as mock_input:
        with patch("main.history.list_history_entries") as mock_list_history:
            with patch("builtins.print") as mock_print:
                mock_list_history.return_value = []
                mock_input.side_effect = ["3", "1", "4"]

                main.main()

                mock_print.assert_any_call("No history yet!")

def test_view_filtered_history():
    with patch("main.history.get_history_by_topic") as mock_history_by_topic:
        with patch("builtins.input", side_effect = ["3", "2", "classes", "4"]):
            with patch("builtins.print") as mock_print:
                mock_history_by_topic.return_value = [
                    {
                        "topic": "classes",
                        "question": "what is inheritance?",
                        "answer": "Inheritance allows a class to inherit from another class."
                    }
                ]

                main.main()

                mock_history_by_topic.assert_called_once_with(main.data, "classes")

                mock_print.assert_any_call("\nTopic: classes")
                mock_print.assert_any_call("Question: what is inheritance?")
                mock_print.assert_any_call("Answer: Inheritance allows a class to inherit from another class.")

def test_view_history_invalid_input():
    with patch("builtins.input", side_effect = ["3", "7", "4"]):
        with patch("builtins.print") as mock_print:
            main.main()
            mock_print.assert_any_call("Invalid option!")

def test_view_history_counts_by_topic_sorted():
    with patch("builtins.input", side_effect = ["3", "3", "4"]):
        with patch("main.history.count_history_by_topics") as mock_count:
            with patch("main.history.sort_topics_counts_descending") as mock_sorted:
                with patch("builtins.print") as mock_print:
                    mock_count.return_value = {"recursion": 2, "classes": 1}
                    mock_sorted.return_value = [("recursion", 2), ("classes", 1)]

                    main.main()

                    mock_count.assert_called_once_with(main.data)
                    mock_sorted.assert_called_once_with(mock_count.return_value)

                    mock_print.assert_any_call("recursion: 2")
                    mock_print.assert_any_call("classes: 1")

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
    with patch("builtins.input", side_effect = ["1", "5", "4"]):
        with patch("builtins.print") as mock_print:

            main.main()

            mock_print.assert_any_call("4. Change topic status")

def test_main_change_topic_status():
    with patch("builtins.input", side_effect = ["1", "4", "recursion", "in progress", "5", "4"]):
        with patch("main.topics.change_topic_status") as mock_change_status:
            with patch("builtins.print") as mock_print:
                mock_change_status.return_value = (True, "changed")

                main.main()

                mock_change_status.assert_called_once_with(main.data, "recursion", "in progress")
                mock_print.assert_any_call("Status changed!")

@pytest.mark.parametrize(
    "change_status, reason, expected_message", 
    [(False, "invalid status", "Invalid status!"), 
    (False, "topic not found", "Topic not found!")])
def test_main_change_topic_status_unsuccessful(change_status, reason, expected_message):
    with patch("builtins.input", side_effect = ["1", "4", "recursion", "in progress", "5", "4"]):
        with patch("main.topics.change_topic_status") as mock_change_status:
            with patch("builtins.print") as mock_print:
                mock_change_status.return_value = (change_status, reason)

                main.main()

                mock_change_status.assert_called_once_with(main.data, "recursion", "in progress")
                mock_print.assert_any_call(expected_message)





            







            

