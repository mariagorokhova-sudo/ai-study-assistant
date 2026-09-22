import menu_utils
from unittest.mock import patch
import pytest

def test_print_numbered_topics():
    topic_names_list = ["Recursion", "Classes"]
    with patch("builtins.print") as mock_print:

        menu_utils.print_numbered_topics(topic_names_list)

        mock_print.assert_any_call("1. Recursion")
        mock_print.assert_any_call("2. Classes")

def test_choose_topic_from_enumerated_list():
    topic_names_list = ["Recursion", "Classes"]
    with patch("builtins.input", side_effect=["2"]):
        result = menu_utils.choose_topic_from_enumerated_list(topic_names_list)

        assert result == "Classes"


@pytest.mark.parametrize("wrong_input", ["abc", "99", "0"])
def test_choose_topic_from_enumerated_list_wrong_input(wrong_input):
    topic_names_list = ["Recursion", "Classes"]
    with patch("builtins.input", side_effect=wrong_input):
        with patch("builtins.print") as mock_print:
            menu_utils.choose_topic_from_enumerated_list(topic_names_list)

            mock_print.assert_any_call("Invalid option!\n")

def test_choose_topic_from_enumerated_list_empty_list():
    topic_names_list = []
    with patch("builtins.print") as mock_print:
        result = menu_utils.choose_topic_from_enumerated_list(topic_names_list)

        assert result is None
        mock_print.assert_any_call("No topics yet!\n")

def test_print_numbered_topics_with_details():
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
    with patch("builtins.print") as mock_print:
        menu_utils.print_numbered_topics_with_details(data)

        mock_print.assert_any_call("1. recursion")
        mock_print.assert_any_call("Status: in progress")
        mock_print.assert_any_call("Notes:")
        mock_print.assert_any_call("- note 1")
        mock_print.assert_any_call("- note 2")
        mock_print.assert_any_call("2. classes")
        mock_print.assert_any_call("Status: new")
        mock_print.assert_any_call("Notes: no notes yet!\n")

def test_print_history_entries_empty_list():
    entries_list = []
    with patch("builtins.print") as mock_print:
        
        menu_utils.print_history_entries(entries_list)

        mock_print.assert_any_call("No history on this topic yet!\n")

def test_print_history_entries():
    entries_list = [
        {
            "topic": "classes",
            "question": "what is inheritance?",
            "answer": "Inheritance allows a class to inherit from another class."
        },
        {
            "topic": "recursion",
            "question": "what is a base case?",
            "answer": "A **base case** tells a recursive function when to stop calling itself."
        }
    ]
    with patch("builtins.print") as mock_print:
        menu_utils.print_history_entries(entries_list)

        mock_print.assert_any_call("\nTopic: classes")
        mock_print.assert_any_call("Question: what is inheritance?")
        mock_print.assert_any_call("Answer: Inheritance allows a class to inherit from another class.")
        mock_print.assert_any_call("\nTopic: recursion")
        mock_print.assert_any_call("Question: what is a base case?")
        mock_print.assert_any_call("Answer: A **base case** tells a recursive function when to stop calling itself.")
