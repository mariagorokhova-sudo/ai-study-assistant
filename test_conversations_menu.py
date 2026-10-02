import conversations_menu
from unittest.mock import patch, call
import pytest
import httpx
import openai

def test_conversations_menu_back_option():
    data = {"topics": [], "conversations": []}
    with patch("builtins.input", side_effect=["6"]):
        conversations_menu.manage_conversations_menu(data)


def test_view_history_invalid_input():
    data = {"topics": [],  "conversations": []}
    with patch("builtins.input", side_effect = ["1", "7", "6"]):
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
    with patch("builtins.input", side_effect = ["2", wrong_choice, "6"]):
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

    with patch("builtins.input", side_effect=["1", "6"]):
        with patch("conversations_menu.menu_utils.print_numbered_conversations") as mock_numbered_print:

            conversations_menu.manage_conversations_menu(data)

            mock_numbered_print.assert_called_once_with(data["conversations"], include_new_option=False)


def test_conversations_menu_print_conversations_topics_list_empty_list():
    data = {
        "topics": [],
        
        "conversations": []
    }
    with patch("builtins.input", side_effect = ["2", "6"]):
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

    with patch("builtins.input", side_effect = ["2", "1", "1", "6"]):
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

    with patch("builtins.input", side_effect = ["3", "6"]):
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
    with patch("builtins.input", side_effect = ["3", "6"]):
        with patch("conversations_menu.conversations.count_conversations_by_topic") as mock_count:
            with patch("conversations_menu.conversations.sort_conversations_counts_descending") as mock_sort:
                with patch("builtins.print") as mock_print:
                    mock_count.return_value = {}

                    conversations_menu.manage_conversations_menu(data)

                    mock_print.assert_any_call("No conversations yet!\n")
                    mock_sort.assert_not_called()


def test_conversations_menu_delete_conversation_success():
    data = {
        "topics": [],
        "conversations": [
            {
            "topic": "Recursion",
            "ai_mode": "Socratic tutor",
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
            }
        ]
    }
    with patch("builtins.input", side_effect = ["5", "1", "6"]):
        with patch("conversations_menu.conversations.delete_conversation") as mock_delete:
            with patch("builtins.print") as mock_print:
                mock_delete.return_value = (True, "deleted")

                conversations_menu.manage_conversations_menu(data)

                mock_delete.assert_called_once_with(data, 0)
                mock_print.assert_any_call("Conversation deleted!\n")


def test_conversations_menu_delete_conversation_empty_list():
    data = {"topics": [], "conversations": []}
    with patch("builtins.input", side_effect = ["5", "6"]):
        with patch("conversations_menu.menu_utils.choose_from_numbered_list") as mock_choose:
            with patch("conversations_menu.conversations.delete_conversation") as mock_delete:

                conversations_menu.manage_conversations_menu(data)

                mock_choose.assert_not_called()
                mock_delete.assert_not_called()


def test_conversations_menu_delete_conversation_invalid_choice():
    data = {
        "topics": [],
        "conversations": [
            {
            "topic": "Recursion",
            "ai_mode": "Socratic tutor",
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
            }
        ]
    }
    with patch("builtins.input", side_effect = ["5", "3", "6"]):
        with patch("conversations_menu.conversations.delete_conversation") as mock_delete:

            conversations_menu.manage_conversations_menu(data)

            mock_delete.assert_not_called()


def test_conversations_menu_summarize_conversation_success():
    data = {
        "topics": [
            {
                "name": "Recursion",
                "status": "new",
                "notes": []
            }
        ],
        "conversations": [
            {
            "topic": "Recursion",
            "ai_mode": "Socratic tutor",
            "messages": [
                {"role": "user",
                "content": "What is recursion?"},
                {"role": "assistant",
                "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
            }
        ]
    }
    with patch("builtins.input", side_effect = ["4", "1", "6"]):
        with patch("conversations_menu.ai.summarize_conversation") as mock_summary:
            with patch("conversations_menu.topics.add_note") as mock_add_note:
                with patch("builtins.print") as mock_print:
                    mock_summary.return_value = "Recursion solves a problem by reducing it to smaller instances."
                    mock_add_note.return_value = (True, "added")

                    conversations_menu.manage_conversations_menu(data)

                    mock_summary.assert_called_once_with(data["conversations"][0])
                    mock_add_note.assert_called_once_with(data, "Recursion", mock_summary.return_value)
                    mock_print.assert_any_call("Conversation summary added as a note!")


def test_conversations_menu_summarize_conversation_no_summary():
    data = {
        "topics": [],
        "conversations": [
            {
            "topic": "Recursion",
            "ai_mode": "Socratic tutor",
            "messages": [
                {"role": "user",
                "content": "What is recursion?"},
                {"role": "assistant",
                "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
            }
        ]
    }
    with patch("builtins.input", side_effect = ["4", "1", "6"]):
        with patch("conversations_menu.ai.summarize_conversation") as mock_summary:
            with patch("conversations_menu.topics.add_note") as mock_add_note:
                with patch("builtins.print") as mock_print:
                    mock_summary.return_value = None

                    conversations_menu.manage_conversations_menu(data)

                    mock_add_note.assert_not_called()
                    mock_print.assert_any_call("Cannot summarize an empty conversation!\n")


def test_conversations_menu_summarize_conversation_no_conversations():
    data = {"topics": [], "conversations": []}
    with patch("builtins.input", side_effect = ["4", "6"]):
        with patch("conversations_menu.ai.summarize_conversation") as mock_summary:
            with patch("conversations_menu.topics.add_note") as mock_add_note:

                conversations_menu.manage_conversations_menu(data)

                mock_summary.assert_not_called()
                mock_add_note.assert_not_called()


def test_conversations_menu_summarize_conversation_no_topic():
    data = {
        "topics": [],
        "conversations": [
            {
            "topic": "Recursion",
            "ai_mode": "Socratic tutor",
            "messages": [
                {"role": "user",
                "content": "What is recursion?"},
                {"role": "assistant",
                "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
            }
        ]
    }
    with patch("builtins.input", side_effect = ["4", "1", "6"]):
        with patch("conversations_menu.ai.summarize_conversation") as mock_summary:
            with patch("conversations_menu.topics.add_note") as mock_add_note:
                with patch("builtins.print") as mock_print:
                    mock_summary.return_value = "Recursion solves a problem by reducing it to smaller instances."
                    mock_add_note.return_value = (False, "topic not found")

                    conversations_menu.manage_conversations_menu(data)

                    mock_print.assert_any_call("Topic not found, cannot add a note!\n")


def test_create_summary_ai_api_error():
    data = {
        "topics": [],
        "conversations": [
            {
            "topic": "Recursion",
            "ai_mode": "Socratic tutor",
            "messages": [
                {"role": "user",
                "content": "What is recursion?"},
                {"role": "assistant",
                "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
            }
        ]
    }
    with patch("builtins.input", side_effect = ["4", "1", "6"]) as mock_input:
        with patch("conversations_menu.ai.summarize_conversation") as mock_summary:
            with patch("conversations_menu.topics.add_note") as mock_add_note:
                with patch("builtins.print") as mock_print:
                    request = httpx.Request("POST", "https://api.openai.com/v1/responses")
                    mock_summary.side_effect = openai.APIConnectionError(request=request)

                    conversations_menu.manage_conversations_menu(data)

                    mock_print.assert_any_call("Sorry, the AI request failed. Please try again.")
                    mock_add_note.assert_not_called()


def test_create_summary_missing_api_key():
    data = {
        "topics": [],
        "conversations": [
            {
            "topic": "Recursion",
            "ai_mode": "Socratic tutor",
            "messages": [
                {"role": "user",
                "content": "What is recursion?"},
                {"role": "assistant",
                "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
            }
        ]
    }
    with patch("builtins.input", side_effect = ["4", "1", "6"]) as mock_input:
        with patch("conversations_menu.ai.summarize_conversation") as mock_summary:
            with patch("builtins.print") as mock_print:
                mock_summary.side_effect = ValueError("OPENAI_API_KEY is missing")

                conversations_menu.manage_conversations_menu(data)

                mock_print.assert_any_call("OPENAI_API_KEY is missing. Please add it to the .env file.")