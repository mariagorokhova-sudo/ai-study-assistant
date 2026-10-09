import topics_menu
import topics
from unittest.mock import patch
import pytest

def test_topics_menu_does_not_change_topics_data():
    data = {
        "courses": [],
        "topics": [
            {
                "name": "recursion",
                "course_statuses": {},
                "notes": ["note 1", "note 2"]
            }
        ],
        "conversations": []
    }
    original_topics = data["topics"].copy()
    with patch("builtins.input", side_effect = ["3"]):

        topics_menu.manage_topics_menu(data)

        assert data["topics"] == original_topics


def test_topics_menu_add_new_topic_no_topics_yet():
    data = {"courses": [], "topics":[], "conversations": []}
    with patch("builtins.input", side_effect = ["1", "Test topic", "2"]):
        with patch("topics_menu.topics.add_topic", return_value = (True, "added")) as mock_add_topic:

            topics_menu.manage_topics_menu(data)

            mock_add_topic.assert_called_once_with(data, "Test topic")


def test_topics_menu_choose_topic_from_list():
    data = {
        "courses": [],
        "topics": [
            {
                "name": "recursion",
                "course_statuses": {},
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
    with patch("builtins.input", side_effect = ["1", "4"]):
        with patch("topics_menu.manage_topic_details_menu") as mock_topic_details:

            topics_menu.manage_topics_menu(data)

            mock_topic_details.assert_called_once_with(data, data["topics"][0])


def test_manage_topic_details_delete_note_empty_notes():
    data = {
        "courses": [],
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {},
                "notes": []
            }
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect=["3", "8"]):
        with patch("topics_menu.topics.delete_note") as mock_delete_note:
            with patch("builtins.print") as mock_print:

                topics_menu.manage_topic_details_menu(data, data["topics"][0])

                mock_delete_note.assert_not_called()
                mock_print.assert_any_call("No notes for this topic yet!\n")


def test_manage_topic_details_delete_note_incorrect_index():
    data = {
        "courses": [],
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {},
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect=["3", "3", "8"]):
        with patch("topics_menu.topics.delete_note") as mock_delete_note:

            topics_menu.manage_topic_details_menu(data, data["topics"][0])

            mock_delete_note.assert_not_called()


def test_manage_topic_details_menu_actions_list():
    data = {
            "topics":[
                {
                    "name": "Recursion",
                    "course_statuses": {},
                    "notes": []
                }
            ],
            "conversations": [
                {
                    "topic": "Recursion",
                    "ai_mode": "Tutor",
                    "messages": [
                        {
                            "role": "user",
                            "content": "what is recursion?"
                        }
                    ]
                }
            ]
        }
    with patch("builtins.input", side_effect=["8"]):
        with patch("topics_menu.menu_utils.print_numbered_list") as mock_list:
            actions_list = ["View notes", "Add note", "Delete note", "Change status", "View conversations", "View courses", "Delete topic", "Back"]
            topics_menu.manage_topic_details_menu(data, data["topics"][0])

            mock_list.assert_called_once_with(actions_list)


def test_manage_topic_details_menu_show_topic_card():
    data = {
            "topics":[
                {
                    "name": "Recursion",
                    "course_statuses": {},
                    "notes": []
                }
            ],
            "conversations": [
                {
                    "topic": "Recursion",
                    "ai_mode": "Tutor",
                    "messages": [
                        {
                            "role": "user",
                            "content": "what is recursion?"
                        }
                    ]
                }
            ]
        }
    with patch("builtins.input", side_effect=["8"]):
        with patch("topics_menu.topics.show_topic_card") as mock_card:

            topics_menu.manage_topic_details_menu(data, data["topics"][0])

            mock_card.assert_called_once_with(data, data["topics"][0])


def test_manage_topic_details_view_notes():
    data = {
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {},
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect=["1", "8"]):
        with patch("topics_menu.menu_utils.print_numbered_list") as mock_list:

            topics_menu.manage_topic_details_menu(data, data["topics"][0])

            mock_list.assert_any_call(data["topics"][0]["notes"], separator=True)


def test_manage_topic_details_add_note():
    data = {
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {},
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect=["2", "new note on recursion", "8"]):
        with patch("topics_menu.topics.add_note", return_value = (True, "added")) as mock_note:

           topics_menu.manage_topic_details_menu(data, data["topics"][0])

           mock_note.assert_called_once_with(data, "Recursion", "new note on recursion")


def test_manage_topic_details_delete_note():
    data = {
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {},
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect=["3", "1", "y", "8"]):
        with patch("topics_menu.topics.delete_note", return_value = (True, "deleted")) as mock_delete:

            topics_menu.manage_topic_details_menu(data, data["topics"][0])

            mock_delete.assert_called_once_with(data, "Recursion", 0)


def test_manage_topic_details_change_status():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            }
        ],
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {"CM1035-01": "learning"},
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect=["4", "1", "1", "8"]):
        with patch("topics_menu.topics.change_topic_course_status", return_value = (True, "changed")) as mock_change_status:

            topics_menu.manage_topic_details_menu(data, data["topics"][0])

            mock_change_status.assert_called_once_with(data, "Recursion", "CM1035-01", "exam prep")


def test_manage_topic_details_change_status_empty_course_statuses():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            }
        ],
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {},
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect=["4", "8"]):
        with patch("topics_menu.topics.change_topic_course_status",) as mock_change_status:
            with patch("builtins.print") as mock_print:

                topics_menu.manage_topic_details_menu(data, data["topics"][0])

                mock_change_status.assert_not_called()
                mock_print.assert_any_call("This topic is not assigned to any course!\n")


def test_manage_topic_details_view_conversations():
    data = {
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {},
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
    with patch("builtins.input", side_effect=["5", "3", "8"]):
        with patch("topics_menu.conversations.get_conversations_by_topic") as mock_get_conversations:
            with patch("topics_menu.menu_utils.print_numbered_conversations") as mock_print_conversations:
                mock_get_conversations.return_value = [
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

                topics_menu.manage_topic_details_menu(data, data["topics"][0])

                mock_get_conversations.assert_called_once_with(data, "Recursion")
                mock_print_conversations.assert_called_once_with(mock_get_conversations.return_value, include_back_option=True)


def test_manage_topic_details_view_conversations_no_conversations():
    data = {
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {},
                "notes": []
            }
        ],
        "conversations": [],
        "courses": []
    }
    with patch("builtins.input", side_effect=["5", "8"]):
        with patch("topics_menu.conversations.get_conversations_by_topic", return_value = []) as mock_get_conversations:
            with patch("topics_menu.menu_utils.print_numbered_conversations") as mock_print_conversations:
                with patch("builtins.print") as mock_print:

                    topics_menu.manage_topic_details_menu(data, data["topics"][0])

                    mock_print_conversations.assert_not_called()
                    mock_print.assert_any_call("No conversations for this topic yet!\n")


def test_manage_topic_details_manage_course_details():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            },
            {
                "code": "CM1005-01",
                "name": "Introduction to Programming I",
                "session": "October 2026 - March 2027",
                "status": "active"
            }
        ],
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {"CM1035-01": "learning", "CM1005-01": "learning"},
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect=["6", "2", "8"]):
        with patch("topics_menu.courses_menu.manage_course_details_menu") as mock_course_details:
        
            topics_menu.manage_topic_details_menu(data, data["topics"][0])

            mock_course_details.assert_called_once_with(data, data["courses"][1])


def test_manage_topic_details_no_courses_to_view():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            },
            {
                "code": "CM1005-01",
                "name": "Introduction to Programming I",
                "session": "October 2026 - March 2027",
                "status": "active"
            }
        ],
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {},
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect=["6", "8"]):
        with patch("topics_menu.courses_menu.manage_course_details_menu") as mock_course_details:
            with patch("builtins.print") as mock_print:
        
                topics_menu.manage_topic_details_menu(data, data["topics"][0])

                mock_course_details.assert_not_called()
                mock_print.assert_any_call("This topic is not assigned to any course!\n")


def test_manage_topic_details_delete_topic():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            }
        ],
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {},
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect=["7", "y"]):
        with patch("topics_menu.topics.delete_topic", return_value = (True, "deleted")) as mock_delete:
            with patch("builtins.print") as mock_print:

                topics_menu.manage_topic_details_menu(data, data["topics"][0])

                mock_delete.assert_called_once_with(data, "Recursion")
                mock_print.assert_any_call("Topic deleted!\n")


def test_manage_topic_details_delete_topic_unsuccess_has_conversations():
    data = {
        "topics":[
            {
                "name": "recursion",
                "course_statuses": {},
                "notes": []
            }
        ],
        "conversations": [
            {
                "topic": "recursion",
                "ai_mode": "Tutor",
                "messages": [
                    {
                        "role": "user",
                        "content": "what is recursion?"
                    }
                ]
            }
        ]
    }
    with patch("builtins.input", side_effect=["7", "y", "8"]):
        with patch("menu_utils.print_numbered_list") as mock_print_numbered_topics:
            with patch("topics_menu.topics.delete_topic", return_value = (False, "topic has conversations")) as mock_delete:
                with patch("builtins.print") as mock_print:

                    topics_menu.manage_topic_details_menu(data, data["topics"][0])

                    mock_delete.assert_called_once_with(data, "recursion")
                    mock_print.assert_any_call("This topic has conversations associated, not possible to delete!\n")


def test_manage_topic_details_delete_topic_option_no_confirmation():
    data = {
        "courses": [],
        "topics":[
            {
                "name": "recursion",
                "course_statuses": {},
                "notes": []
            }
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect=["7", "n", "8"]):
        with patch("topics_menu.topics.delete_topic") as mock_delete:

            topics_menu.manage_topic_details_menu(data, data["topics"][0])

            mock_delete.assert_not_called()


def test_manage_topic_details_manage_conversation_details():
    data = {
        "topics":[
            {
                "name": "recursion",
                "course_statuses": {},
                "notes": []
            }
        ],
        "conversations": [
            {
                "topic": "recursion",
                "ai_mode": "Tutor",
                "messages": [
                    {
                        "role": "user",
                        "content": "what is recursion?"
                    }
                ]
            }
        ]
    }
    with patch("builtins.input", side_effect = ["5", "1", "8"]):
        with patch("topics_menu.conversations_menu.manage_conversation_details_menu") as mock_conversation_details:

            topics_menu.manage_topic_details_menu(data, data["topics"][0])

            mock_conversation_details.assert_called_once_with(data, data["conversations"][0])