import history_menu
import history
from unittest.mock import patch, call
import pytest

def test_history_menu_back_option():
    data = {"topics": [], "history": []}
    with patch("builtins.input", side_effect=["4"]):
        history_menu.manage_history_menu(data)

def test_view_history_invalid_input():
    data = {"topics": [], "history": [], "conversations": []}
    with patch("builtins.input", side_effect = ["1", "7", "4"]):
        with patch("builtins.print") as mock_print:
            history_menu.manage_history_menu(data)
            mock_print.assert_any_call("Invalid option!\n")

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
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect = ["2", "4"]):
        with patch("history.get_unique_history_topics") as mock_unique_history_set:
            with patch("history_menu.menu_utils.choose_from_numbered_list") as mock_choose_topic:
                with patch("history_menu.history.get_history_by_topic") as mock_history:
                    mock_unique_history_set.return_value = {"recursion", "classes"}
                    mock_choose_topic.return_value = "recursion"

                    history_menu.manage_history_menu(data)


                    mock_choose_topic.assert_called_once_with(["classes", "recursion"])
                    mock_history.assert_called_once_with(data, "recursion")

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
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect = ["2", wrong_choice, "4"]):
        with patch("history_menu.history.get_history_by_topic") as mock_history:

            history_menu.manage_history_menu(data)

            mock_history.assert_not_called()

def test_history_menu_print_numbered_conversations():
    data = {
        "topics": [],
        "history": [],
        "conversations": [
                {
            "topic": "recursion", 
            "ai_mode": "socratic tutor", 
            "messages": [
                {"role": "user",
                "content": "What is base case?"},
                {"role": "assistant",
                "content": "Base case is ..."},
                {"role": "user",
                "content": "What is recursion?"},
                {"role": "assistant",
                "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
            }
        ]
    }

    with patch("builtins.input", side_effect=["1", "4"]):
        with patch("history_menu.menu_utils.print_numbered_conversations") as mock_numbered_print:

            history_menu.manage_history_menu(data)

            mock_numbered_print.assert_called_once_with(data["conversations"], include_new_option=False)

def test_history_menu_print_conversations_topics_list_empty_list():
    data = {
        "topics": [],
        "history": [],
        "conversations": []
    }
    with patch("builtins.input", side_effect = ["2", "4"]):
        with patch("history_menu.conversations.get_unique_conversations_topics") as mock_topics_list:
            with patch("builtins.print") as mock_print:
                mock_topics_list.return_value = []

                history_menu.manage_history_menu(data)

                mock_print.assert_any_call("No conversations yet!\n")

def test_history_menu_view_history_on_specific_topic():
    data = {
        "topics": [],
        "history": [],
        "conversations": [
            {
                "topic": "recursion", 
                "ai_mode": "socratic tutor", 
                "messages": [
                    {"role": "user",
                    "content": "What is base case?"},
                    {"role": "assistant",
                    "content": "Base case is ..."}
                ]
            }
        ]
    }

    with patch("builtins.input", side_effect = ["2", "1", "1", "4"]):
        with patch("history_menu.menu_utils.print_all_conversation_messages") as mock_print_all_messages:

            history_menu.manage_history_menu(data)

            mock_print_all_messages.assert_called_once_with(data["conversations"][0])

def test_history_menu_view_conversations_counts():
    data = {
        "topics": [], 
        "history": [], 
        "conversations": [
            {
            "topic": "recursion", 
            "ai_mode": "socratic tutor", 
            "messages": [
                {"role": "user",
                "content": "What is recursion?"},
                {"role": "assistant",
                "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
            },
            {
            "topic": "Recursion", 
            "ai_mode": "Debugger", 
            "messages": [
                {"role": "user",
                "content": "Question on debugging?"},
                {"role": "assistant",
                "content": "Answer on debugging"}]
            },
            {
                "topic": "classes", 
                "ai_mode": "socratic tutor", 
                "messages": [
                    {"role": "user",
                    "content": "What is inheritance"},
                    {"role": "assistant",
                    "content": "Inheritance lets one class reuse another class."}]
            }
        ]
    }

    with patch("builtins.input", side_effect = ["3", "4"]):
        with patch("history_menu.conversations.count_conversations_by_topic") as mock_count:
            with patch("history_menu.conversations.sort_conversations_counts_descending") as mock_sort:
                with patch("builtins.print") as mock_print:
                    mock_count.return_value = {
                        "classes": 1,
                        "recursion": 2
                    }

                    mock_sort.return_value = [("recursion", 2), ("classes", 1)]

                    history_menu.manage_history_menu(data)

                    mock_count.assert_called_once_with(data)
                    mock_sort.assert_called_once_with(mock_count.return_value)
                    mock_print.assert_has_calls([call("recursion: 2"), call("classes: 1")])

def test_history_menu_view_conversations_counts_empty_conversations():
    data = {
        "topics": [], 
        "history": [], 
        "conversations": []
    }
    with patch("builtins.input", side_effect = ["3", "4"]):
        with patch("history_menu.conversations.count_conversations_by_topic") as mock_count:
            with patch("history_menu.conversations.sort_conversations_counts_descending") as mock_sort:
                with patch("builtins.print") as mock_print:
                    mock_count.return_value = {}

                    history_menu.manage_history_menu(data)

                    mock_print.assert_any_call("No conversations yet!\n")
                    mock_sort.assert_not_called()



    



        







