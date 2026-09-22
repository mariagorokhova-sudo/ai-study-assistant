import history_menu
import history
from unittest.mock import patch
import pytest

def test_history_menu_back_option():
    data = {"topics": [], "history": []}
    with patch("builtins.input", side_effect=["4"]):
        history_menu.manage_history_menu(data)

def test_view_history():
    data = {"topics": [], "history": []}
    with patch("builtins.input") as mock_input:
        with patch("history_menu.history.list_history_entries") as mock_list_history:
            with patch("builtins.print") as mock_print:
                mock_list_history.return_value = [
                    {
                        "topic": "classes",
                        "question": "what is inheritance?",
                        "answer": "Inheritance allows a class to inherit from another class."
                    }
                ]
                mock_input.side_effect = ["1", "4"]

                history_menu.manage_history_menu(data)

                mock_print.assert_any_call("\nTopic: classes")
                mock_print.assert_any_call("Question: what is inheritance?")
                mock_print.assert_any_call("Answer: Inheritance allows a class to inherit from another class.")

def test_view_empty_history():
    data = {"topics": [], "history": []}
    with patch("builtins.input") as mock_input:
        with patch("history_menu.history.list_history_entries") as mock_list_history:
            with patch("history_menu.menu_utils.print_history_entries") as mock_print:
                mock_list_history.return_value = []
                mock_input.side_effect = ["1", "4"]

                history_menu.manage_history_menu(data)

                mock_print.assert_called_once_with([])

def test_view_filtered_history():
    data = {"topics": [], "history": [
            {
                "topic": "classes",
                "question": "what is inheritance?",
                "answer": "Inheritance allows a class to inherit from another class."
            }
        ]
    }
    with patch("history_menu.history.get_history_by_topic") as mock_history_by_topic:
        with patch("builtins.input", side_effect = ["2", "4"]):
            with patch("history_menu.menu_utils.choose_topic_from_enumerated_list") as mock_choice:
                with patch("history_menu.menu_utils.print_history_entries") as mock_print:
                    mock_choice.return_value = "classes"
                    mock_history_by_topic.return_value = [
                        {
                            "topic": "classes",
                            "question": "what is inheritance?",
                            "answer": "Inheritance allows a class to inherit from another class."
                        }
                    ]

                    history_menu.manage_history_menu(data)

                    mock_choice.assert_called_once_with(["classes"])
                    mock_history_by_topic.assert_called_once_with(data, "classes")
                    mock_print.assert_called_once_with(mock_history_by_topic.return_value)

def test_view_history_invalid_input():
    data = {"topics": [], "history": []}
    with patch("builtins.input", side_effect = ["1", "7", "4"]):
        with patch("builtins.print") as mock_print:
            history_menu.manage_history_menu(data)
            mock_print.assert_any_call("Invalid option!\n")

def test_view_history_counts_by_topic_sorted():
    data = {"topics": [], "history": []}
    with patch("builtins.input", side_effect = ["3", "4"]):
        with patch("history_menu.history.count_history_by_topics") as mock_count:
            with patch("history_menu.history.sort_topics_counts_descending") as mock_sorted:
                with patch("builtins.print") as mock_print:
                    mock_count.return_value = {"recursion": 2, "classes": 1}
                    mock_sorted.return_value = [("recursion", 2), ("classes", 1)]

                    history_menu.manage_history_menu(data)

                    mock_count.assert_called_once_with(data)
                    mock_sorted.assert_called_once_with(mock_count.return_value)

                    mock_print.assert_any_call("recursion: 2")
                    mock_print.assert_any_call("classes: 1")

def test_history_menu_view_history_on_specific_topic():
    data = {
        "topics": [], 
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
    with patch("builtins.input", side_effect = ["2", "4"]):
        with patch("history.get_unique_history_topics") as mock_unique_history_set:
            with patch("history_menu.menu_utils.choose_topic_from_enumerated_list") as mock_choose_topic:
                with patch("history_menu.history.get_history_by_topic") as mock_history:
                    mock_unique_history_set.return_value = {"recursion", "classes"}
                    mock_choose_topic.return_value = "recursion"

                    history_menu.manage_history_menu(data)


                    mock_choose_topic.assert_called_once_with(["classes", "recursion"])
                    mock_history.assert_called_once_with(data, "recursion")

def test_history_menu_view_history_on_specific_topic_empty_history():
    data = {"topics":[], "history": []}
    with patch("builtins.input", side_effect = ["2", "4"]):
        with patch("builtins.print") as mock_print:
            with patch("history_menu.menu_utils.print_numbered_topics") as mock_print_numbererd_topics:

                history_menu.manage_history_menu(data)

                mock_print.assert_any_call("No history yet!\n")
                mock_print_numbererd_topics.assert_not_called()

@pytest.mark.parametrize("wrong_choice", ["abc", "0", "99"])
def test_view_history_by_topic_wrong_topic_choice(wrong_choice):
    data = {
        "topics": [], 
        "history": [
            {
                "topic": "classes",
                "question": "what is inheritance?",
                "answer": "Inheritance allows a class to inherit from another class."
            }
        ]
    }
    with patch("builtins.input", side_effect = ["2", wrong_choice, "4"]):
        with patch("history_menu.history.get_history_by_topic") as mock_history:

            history_menu.manage_history_menu(data)

            mock_history.assert_not_called()




