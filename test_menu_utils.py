import menu_utils
from unittest.mock import patch, call
import pytest

def test_print_numbered_list():
    topic_names_list = ["Recursion", "Classes"]
    with patch("builtins.print") as mock_print:

        menu_utils.print_numbered_list(topic_names_list)

        mock_print.assert_any_call("1. Recursion")
        mock_print.assert_any_call("2. Classes")


def test_choose_from_numbered_list():
    topic_names_list = ["Recursion", "Classes"]
    with patch("builtins.input", side_effect=["2"]):
        result = menu_utils.choose_from_numbered_list(topic_names_list)

        assert result == "Classes"


@pytest.mark.parametrize("wrong_input", ["abc", "99", "0"])
def test_choose_from_numbered_list_wrong_input(wrong_input):
    topic_names_list = ["Recursion", "Classes"]
    with patch("builtins.input", return_value=wrong_input):
        with patch("builtins.print") as mock_print:
            menu_utils.choose_from_numbered_list(topic_names_list)

            mock_print.assert_any_call("Invalid option!\n")


def test_choose_from_numbered_list_empty_list():
    topic_names_list = []
    with patch("builtins.print") as mock_print:
        result = menu_utils.choose_from_numbered_list(topic_names_list)

        assert result is None
        mock_print.assert_any_call("No options yet!\n")


def test_print_numbered_topics_with_details():
    data = {
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {"CM1005-01": "learning", "CM1035-01": "exam prep"},
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
    with patch("builtins.print") as mock_print:
        menu_utils.print_numbered_topics_with_details(data)

        mock_print.assert_any_call("1. Recursion\n")
        mock_print.assert_any_call("Course statuses:")
        mock_print.assert_any_call("- CM1005-01: learning")
        mock_print.assert_any_call("- CM1035-01: exam prep")
        mock_print.assert_any_call("Notes:")
        mock_print.assert_any_call("- note 1")
        mock_print.assert_any_call("...................................................................................")
        mock_print.assert_any_call("- note 2")
        mock_print.assert_any_call("2. classes\n")
        mock_print.assert_any_call("Topic is not assigned to any courses.\n")
        mock_print.assert_any_call("Notes: no notes yet!\n")


def test_print_numbered_conversations():
    conversations_list = [{
        "topic": "recursion", 
        "ai_mode": "Socratic tutor", 
        "messages": [
            {"role": "user",
            "content": "What is recursion?"},
            {"role": "assistant",
            "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
        }] 
    with patch("builtins.print") as mock_print:
        
        menu_utils.print_numbered_conversations(conversations_list)

        mock_print.assert_any_call("1. Topic: recursion | AI mode: Socratic tutor | Last question: What is recursion?")
        mock_print.assert_any_call("2. Start new conversation\n")


def test_print_numbered_conversations_empty_list():
    conversations_list = []
    with patch("builtins.print") as mock_print:
        menu_utils.print_numbered_conversations(conversations_list)

        mock_print.assert_any_call("No conversations yet!\n")


def test_print_all_conversation_messages():
    conversation_entry = {
        "topic": "recursion",
        "ai_mode": "Socratic tutor",
        "messages": [
            {
                "role": "user",
                "content": "What is recursion?"
            },
            {
                "role": "assistant",
                "content": "It's when a function calls itself."
            }
        ]
    }
    with patch("builtins.print") as mock_print:

        menu_utils.print_all_conversation_messages(conversation_entry)

        mock_print.assert_any_call("AI mode: Socratic tutor")
        mock_print.assert_any_call("User: What is recursion?")
        mock_print.assert_any_call("Assistant: It's when a function calls itself.")


def test_choose_from_numbered_list_without_other_option():
    options_list = [
        {
            "topic": "recursion",
            "ai_mode": "Socratic tutor",
            "messages": [
                {
                    "role": "user",
                    "content": "What is recursion?"
                },
                {
                    "role": "assistant",
                    "content": "It's when a function calls itself."
                }
            ]
        }
    ]

    with patch("builtins.input", side_effect=["1"]):
       result = menu_utils.choose_from_numbered_list(options_list, include_other_option=False)

       assert result == options_list[0]


def test_adding_custom_propmt_to_choose_from_numbered_list():
    topic_list = ["recursion", "classes"]
    with patch("builtins.input", return_value="1") as mock_input:
        result = menu_utils.choose_from_numbered_list(topic_list, prompt="Please choose a topic: ")

        mock_input.assert_called_once_with("Please choose a topic: ")
        assert result == "recursion"


def test_menu_utils_return_index_from_numbered_list():
    notes_list = ["first note", "second note"]
    with patch("builtins.input", return_value="2") as mock_input:
        result = menu_utils.choose_from_numbered_list(notes_list, return_index=True)

        assert result == 1