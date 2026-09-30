import ai
import ai_menu
import openai
import httpx
from unittest.mock import patch, call
import pytest
import conversations

def test_ai_api_error():
    data = {"topics": [],  "conversations": []}
    with patch("builtins.input") as mock_input:
        with patch("ai_menu.topics.list_topics") as mock_list_topics:
            with patch("ai_menu.ai.ask_about_topic") as mock_ask:
                    with patch("ai_menu.conversations.create_conversation", wraps=conversations.create_conversation) as mock_conversation:                     
                        with patch("ai_menu.conversations.add_message_to_conversation", wraps=conversations.add_message_to_conversation) as mock_message:
                            with patch("builtins.print") as mock_print:
                                with patch("ai_menu.conversations.save_conversation") as mock_save:
                                    mock_input.side_effect = [
                                        "1",
                                        "1",
                                        "1",
                                        "what is recursion?",
                                        "/exit"
                                    ]
                                    mock_list_topics.return_value = ["recursion", "classes", "algorythms"]
                                    request = httpx.Request("POST", "https://api.openai.com/v1/responses")
                                    mock_ask.side_effect = openai.APIConnectionError(request=request)
                                    
                                    ai_menu.manage_ai_menu(data)
                                    created_conversation = mock_message.call_args.args[0]

                                    mock_print.assert_any_call("Sorry, the AI request failed. Please try again.")
                                    mock_message.assert_called_once_with(created_conversation, "user", "what is recursion?")
                                    mock_save.assert_called_once_with(data)
                                    assert created_conversation["messages"] == []
                                    assert data["conversations"] == []

def test_ai_request_success_add_messages_to_conversation():
    data = {"topics": [],  "conversations": []}
    with patch("builtins.input") as mock_input:
        with patch("ai_menu.topics.list_topics") as mock_list_topics:
            with patch("ai_menu.ai.ask_about_topic") as mock_ask:
                with patch("ai_menu.topics.get_notes") as mock_notes:
                    with patch("ai_menu.conversations.create_conversation") as mock_conversation:
                        with patch("ai_menu.conversations.add_message_to_conversation") as mock_message:
                            with patch("ai_menu.conversations.save_conversation") as mock_save:
                                mock_input.side_effect = [
                                                "2",
                                                "1",
                                                "2",
                                                "what is inheritance?",
                                                "/exit"
                                            ]
                                mock_list_topics.return_value = ["recursion", "classes", "algorythms"]
                                mock_conversation.return_value = {"topic": "classes", "ai_mode": "Socratic tutor", "messages": []}
                                mock_notes.return_value = ["Note 1"]
                                mock_ask.return_value = "Inheritance allows a class to inherit from another class."

                                ai_menu.manage_ai_menu(data)

                                mock_notes.assert_called_once_with(data, "classes")
                                mock_ask.assert_called_once_with(mock_conversation.return_value, mock_notes.return_value)
                                assert mock_message.call_count == 2
                                mock_message.assert_has_calls([
                                    call(mock_conversation.return_value, "user", "what is inheritance?"),
                                    call(mock_conversation.return_value, "assistant", "Inheritance allows a class to inherit from another class.")
                                    ])
                                mock_save.assert_called_once_with(data)

def test_invalid_topic_input():
    data = {"topics": [],  "conversations": []}
    with patch("builtins.input", side_effect = ["abc"]):
        with patch("ai_menu.ai.ask_about_topic") as mock_ask:
            with patch("ai_menu.topics.list_topics") as mock_list_topics:
                with patch("builtins.print") as mock_print:
                    mock_list_topics.return_value = ["recursion", "classes", "algorythms"]

                    ai_menu.manage_ai_menu(data)

                    mock_print.assert_any_call("Invalid option!\n")
                    mock_ask.assert_not_called()

def test_other_topic_option():
    data = {"topics": [],  "conversations": []}
    with patch("ai_menu.topics.list_topics") as mock_list_topics:
        with patch("builtins.input") as mock_input:
            with patch("ai_menu.ai.ask_about_topic") as mock_ask:
                with patch("ai_menu.topics.get_notes") as mock_notes:
                    with patch("ai_menu.conversations.save_conversation") as mock_save:
                        with patch("ai_menu.topics.add_topic") as mock_add_topic:
                            mock_list_topics.return_value = ["recursion", "classes", "algorythms"]
                            mock_input.side_effect = [
                                "4",
                                "binary trees",
                                "1",
                                "1",
                                "what is a binary tree?",
                                "/exit"
                            ]

                            mock_notes.return_value = []
                            mock_ask.return_value = "A binary tree is a ..."

                            ai_menu.manage_ai_menu(data)

                            mock_ask.assert_called_once_with(
                                data["conversations"][0], [])
                            mock_add_topic.assert_called_once_with(data, "binary trees")

def test_other_topic_option_case_insensitive():
    data = {"topics": [],  "conversations": []}
    with patch("ai_menu.topics.list_topics") as mock_list_topics:
        with patch("builtins.input") as mock_input:
            with patch("ai_menu.ai.ask_about_topic") as mock_ask:
                with patch("ai_menu.topics.get_notes") as mock_notes:
                    with patch("ai_menu.topics.add_topic") as mock_add_topic:
                        with patch("ai_menu.conversations.create_conversation") as mock_create:
                            with patch("ai_menu.conversations.save_conversation") as mock_save:
                                mock_list_topics.return_value = ["Recursion", "Classes", "Algorithms"]
                                mock_input.side_effect = [
                                    "4",
                                    "recursion",
                                    "1",
                                    "1",
                                    "what is a base case?",
                                    "/exit"
                                ]

                                mock_notes.return_value = []
                                mock_ask.return_value = "A base case is a..."
                                mock_add_topic.return_value = False

                                ai_menu.manage_ai_menu(data)

                                mock_create.assert_called_once_with(data, "Recursion", "Tutor")


@pytest.mark.parametrize("edge_choice", ["0", "99"])
def test_invalid_topic_input_edge_cases(edge_choice):
    data = {"topics": [],  "conversations": []}
    with patch("builtins.input", side_effect = [edge_choice]):
        with patch("ai_menu.ai.ask_about_topic") as mock_ask:
            with patch("ai_menu.topics.list_topics") as mock_list_topics:
                with patch("builtins.print") as mock_print:
                    with patch("ai_menu.conversations.save_conversation") as mock_save:
                        mock_list_topics.return_value = ["recursion", "classes", "algorythms"]

                        ai_menu.manage_ai_menu(data)

                        mock_print.assert_any_call("Invalid option!\n")
                        mock_ask.assert_not_called()
                        mock_save.assert_not_called()


def test_ai_menu_create_conversation_success():
    data = {"topics": [],  "conversations": []}
    with patch("ai_menu.topics.list_topics") as mock_list_topics:
        with patch("ai_menu.ai.ask_about_topic") as mock_ask:
            with patch("builtins.input", side_effect = ["2", "1", "2", "what is inheritance?", "/exit"]):
                with patch("ai_menu.conversations.create_conversation") as mock_conversation:
                    with patch("ai_menu.conversations.save_conversation") as mock_save:
                        mock_list_topics.return_value = ["recursion", "classes", "algorithms"]

                        ai_menu.manage_ai_menu(data)

                        mock_conversation.assert_called_once_with(data, "classes", "Socratic tutor")


def test_ai_menu_exit_from_ai_conversation():
    data = {"topics": [],  "conversations": []}
    with patch("ai_menu.topics.list_topics") as mock_list_topics:
        with patch("builtins.input", side_effect = ["2", "2", "/exit"]):
            with patch("ai_menu.ai.ask_about_topic") as mock_ask:
                with patch("ai_menu.conversations.create_conversation") as mock_conversation:
                    with patch("ai_menu.conversations.save_conversation") as mock_save:
                        mock_list_topics.return_value = ["recursion", "classes", "algorithms"]

                        ai_menu.manage_ai_menu(data)

                        mock_ask.assert_not_called()
                        mock_conversation.assert_not_called()
                        mock_save.assert_not_called()


def test_ai_menu_continuing_conversation():
    data = {"topics": [],  "conversations": []}
    with patch("ai_menu.topics.list_topics") as mock_list_topics:
        with patch("builtins.input", side_effect = ["2", "1", "2", "What is inheritance?", "Can you give me an example?", "/exit"]):
            with patch("ai_menu.ai.ask_about_topic") as mock_ask:
                with patch("ai_menu.conversations.create_conversation") as mock_conversation:
                    with patch("ai_menu.conversations.save_conversation") as mock_save:
                        with patch("ai_menu.conversations.add_message_to_conversation") as mock_message:
                            mock_list_topics.return_value = ["recursion", "classes", "algorithms"]
                            mock_ask.side_effect = ["Inheritance lets one class reuse another class",
                                                    "For example, Dog can inherit from Animal"]
                            mock_conversation.return_value = {"topic": "classes", "ai_mode": "Socratic tutor", "messages": []}

                            ai_menu.manage_ai_menu(data)

                            assert mock_ask.call_count == 2
                            mock_ask.assert_has_calls([call(mock_conversation.return_value, None), call(mock_conversation.return_value, None)])
                            assert mock_message.call_count == 4
                            mock_message.assert_has_calls([call(mock_conversation.return_value, "user", "What is inheritance?"),
                                                           call(mock_conversation.return_value, "assistant", "Inheritance lets one class reuse another class"),
                                                           call(mock_conversation.return_value, "user", "Can you give me an example?"),
                                                           call(mock_conversation.return_value, "assistant", "For example, Dog can inherit from Animal")])
                            mock_conversation.assert_called_once_with(data, "classes", "Socratic tutor")
                            assert mock_save.call_count == 2


def test_choose_existing_conversation_to_continue():
    existing_conversation = {
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
    data = {"topics": [],  "conversations": [existing_conversation]}
    with patch("ai_menu.topics.list_topics") as mock_list_topics:
        with patch("builtins.input", side_effect = ["1", "1", "Why do we need a base case?", "/exit"]):
            with patch("ai_menu.conversations.get_conversations_by_topic") as mock_conversations_list:
                with patch("ai_menu.conversations.create_conversation") as mock_conversation:
                    with patch("ai_menu.ai.ask_about_topic") as mock_ask:
                        with patch("ai_menu.conversations.save_conversation") as mock_save:
                            mock_list_topics.return_value = ["recursion", "classes", "algorithms"]
                            mock_conversations_list.return_value = [existing_conversation]
                            mock_ask.return_value = "Without one the function will call itself forever causing the program to crash."

                            ai_menu.manage_ai_menu(data)

                            mock_conversation.assert_not_called()
                            mock_ask.assert_called_once_with(existing_conversation, None)
                            assert existing_conversation["messages"][-2] == {"role": "user",
                                                                             "content": "Why do we need a base case?"}
                            assert existing_conversation["messages"][-1] == {"role": "assistant",
                                                                             "content": "Without one the function will call itself forever causing the program to crash."}
                            mock_save.assert_called_once_with(data)


def test_ai_menu_empty_question():
    data = {"topics": [],  "conversations": []}
    with patch("ai_menu.topics.list_topics") as mock_list_topics:
        with patch("builtins.input", side_effect = ["1", "1", "1", "  ", "/exit"]):
            with patch("ai_menu.ai.ask_about_topic") as mock_ask:
                with patch("ai_menu.conversations.create_conversation") as mock_conversation:
                    with patch("ai_menu.conversations.save_conversation") as mock_save:
                        with patch("ai_menu.conversations.add_message_to_conversation") as mock_message:
                            with patch("builtins.print") as mock_print:
                                mock_list_topics.return_value = ["recursion", "classes", "algorithms"]

                                ai_menu.manage_ai_menu(data)

                                mock_ask.assert_not_called()
                                mock_conversation.assert_not_called()
                                mock_message.assert_not_called()
                                mock_print.assert_any_call("Question cannot be empty, please try again.")