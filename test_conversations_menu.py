import conversations_menu
from unittest.mock import patch, call
import pytest

def test_conversations_menu_back_option():
    data = {"topics": [], "conversations": []}
    with patch("builtins.input", side_effect=["4"]):
        conversations_menu.manage_conversations_menu(data)

def test_view_history_invalid_input():
    data = {"topics": [],  "conversations": []}
    with patch("builtins.input", side_effect = ["1", "7", "4"]):
        with patch("builtins.print") as mock_print:
            conversations_menu.manage_conversations_menu(data)
            mock_print.assert_any_call("Invalid option!\n")

@pytest.mark.parametrize("wrong_choice", ["abc", "0", "99"])
def test_view_history_by_topic_wrong_topic_choice(wrong_choice):
    data = {
        "topics": [], 
        
        "conversations": [
            {
                "topic": "recursion", 
                "ai_mode": "socratic tutor", 
                "messages": [
                    {"role": "user",
                    "content": "What is recursion?"},
                    {"role": "assistant",
                    "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
            }
        ]
    }
    with patch("builtins.input", side_effect = ["2", wrong_choice, "4"]):
        with patch("conversations_menu.conversations.get_conversations_by_topic") as mock_conversations:

            conversations_menu.manage_conversations_menu(data)

            mock_conversations.assert_not_called()

def test_conversations_menu_print_numbered_conversations():
    data = {
        "topics": [],
        
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
        with patch("conversations_menu.menu_utils.print_numbered_conversations") as mock_numbered_print:

            conversations_menu.manage_conversations_menu(data)

            mock_numbered_print.assert_called_once_with(data["conversations"], include_new_option=False)

def test_conversations_menu_print_conversations_topics_list_empty_list():
    data = {
        "topics": [],
        
        "conversations": []
    }
    with patch("builtins.input", side_effect = ["2", "4"]):
        with patch("conversations_menu.conversations.get_unique_conversations_topics") as mock_topics_list:
            with patch("builtins.print") as mock_print:
                mock_topics_list.return_value = []

                conversations_menu.manage_conversations_menu(data)

                mock_print.assert_any_call("No conversations yet!\n")

def test_conversations_menu_view_history_on_specific_topic():
    data = {
        "topics": [],
        
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
        with patch("conversations_menu.menu_utils.print_all_conversation_messages") as mock_print_all_messages:

            conversations_menu.manage_conversations_menu(data)

            mock_print_all_messages.assert_called_once_with(data["conversations"][0])

def test_conversations_menu_view_conversations_counts():
    data = {
        "topics": [], 
         
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
        with patch("conversations_menu.conversations.count_conversations_by_topic") as mock_count:
            with patch("conversations_menu.conversations.sort_conversations_counts_descending") as mock_sort:
                with patch("builtins.print") as mock_print:
                    mock_count.return_value = {
                        "classes": 1,
                        "recursion": 2
                    }

                    mock_sort.return_value = [("recursion", 2), ("classes", 1)]

                    conversations_menu.manage_conversations_menu(data)

                    mock_count.assert_called_once_with(data)
                    mock_sort.assert_called_once_with(mock_count.return_value)
                    mock_print.assert_has_calls([call("recursion: 2"), call("classes: 1")])

def test_conversations_menu_view_conversations_counts_empty_conversations():
    data = {
        "topics": [], 
         
        "conversations": []
    }
    with patch("builtins.input", side_effect = ["3", "4"]):
        with patch("conversations_menu.conversations.count_conversations_by_topic") as mock_count:
            with patch("conversations_menu.conversations.sort_conversations_counts_descending") as mock_sort:
                with patch("builtins.print") as mock_print:
                    mock_count.return_value = {}

                    conversations_menu.manage_conversations_menu(data)

                    mock_print.assert_any_call("No conversations yet!\n")
                    mock_sort.assert_not_called()



    



        







