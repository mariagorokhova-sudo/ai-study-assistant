import courses_menu
from unittest.mock import patch
import pytest
import topics_menu

def test_courses_menu_does_not_change_courses_data():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "October 2026 - May 2027",
                "status": "active"
            }
        ],
        "topics": [],
        "conversations": []
    }
    original_courses = data["courses"].copy()
    with patch("builtins.input", side_effect = ["3"]):

        courses_menu.manage_courses_menu(data)

        assert data["courses"] == original_courses


def test_manage_courses_menu_back():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "October 2026 - May 2027",
                "status": "active"
            }
        ],
        "topics": [],
        "conversations": []
    }
    with patch("builtins.input", side_effect = ["3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:

            courses_menu.manage_courses_menu(data)

            mock_show_card.assert_not_called()


def test_manage_courses_menu_add_course_success():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "October 2026 - May 2027",
                "status": "active"
            }
        ],
        "topics": [],
        "conversations": []
    }
    with patch("builtins.input", side_effect = ["2", "CM1005-01", "Introduction to Programming I", "October 2026 - May 2027", "3"]):
        with patch("courses_menu.courses.add_course", return_value = (True, "added")) as mock_add:
            with patch("builtins.print") as mock_print:

                courses_menu.manage_courses_menu(data)

                mock_add.assert_called_once_with(data, "CM1005-01", "Introduction to Programming I", "October 2026 - May 2027")
                mock_print.assert_any_call(f'\nCourse CM1005-01 - Introduction to Programming I is successfully added!\n')


@pytest.mark.parametrize("reason, expected_message", [("empty field", "\nCourse fields cannot be empty!\n"), ("duplicate", "\nThis course already exists!\n")])
def test_manage_courses_menu_add_course_unsuccess(reason, expected_message):
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "October 2026 - May 2027",
                "status": "active"
            }
        ],
        "topics": [],
        "conversations": []
    }
    with patch("builtins.input", side_effect = ["2", "CM1005-01", "Introduction to Programming I", "October 2026 - May 2027", "3"]):
        with patch("courses_menu.courses.add_course", return_value = (False, reason)) as mock_add:
            with patch("builtins.print") as mock_print:

                courses_menu.manage_courses_menu(data)

                mock_add.assert_called_once_with(data, "CM1005-01", "Introduction to Programming I", "October 2026 - May 2027")
                mock_print.assert_any_call(expected_message)


def test_manage_courses_nenu_courses_actions_back():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "October 2026 - May 2027",
                "status": "active"
            }
        ],
        "topics": [],
        "conversations": []
    }
    with patch("builtins.input", side_effect = ["1", "8", "3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:

            courses_menu.manage_courses_menu(data)

            mock_show_card.assert_called_once_with(data, data["courses"][0])


def test_manage_courses_menu_view_topics():
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
            },
            {
                "name": "Classes",
                "course_statuses": {"CM1035-01": "exam prep"},
                "notes": ["Inheritance is an important concept."]
            },
            {
                "name": "Binary trees",
                "course_statuses": {"CM1035-01": "finished"},
                "notes": ["Binary tree is a..."]
            },
            {
                "name": "Data structures",
                "course_statuses": {"CM1005-01": "learning"},
                "notes": ["Lists and arrays."]
            }
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect = ["1", "1", "5", "8", "3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:
            with patch("courses_menu.topics.show_topics_for_course") as mock_show_topics:

                courses_menu.manage_courses_menu(data)

                mock_show_topics.assert_called_once_with(data, "CM1035-01", include_back=True)


def test_manage_courses_menu_view_topics_manage_topic_details():
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
            },
            {
                "name": "Classes",
                "course_statuses": {"CM1035-01": "exam prep"},
                "notes": ["Inheritance is an important concept."]
            },
            {
                "name": "Binary trees",
                "course_statuses": {"CM1035-01": "finished"},
                "notes": ["Binary tree is a..."]
            },
            {
                "name": "Data structures",
                "course_statuses": {"CM1035-01": "learning"},
                "notes": ["Lists and arrays."]
            }
        ],
        "conversations": []
    }
    with patch("builtins.input", side_effect = ["1", "1", "2", "8", "3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:
            with patch("courses_menu.topics.show_topics_for_course"):
                with patch("courses_menu.topics_menu.manage_topic_details_menu") as mock_topic_details:

                    expected_topic = {
                        "name": "Data structures",
                        "course_statuses": {"CM1035-01": "learning"},
                        "notes": ["Lists and arrays."]
                    }

                    courses_menu.manage_courses_menu(data)

                    mock_topic_details.assert_called_once_with(data, expected_topic)


def test_manage_courses_menu_assign_topic_to_course():
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
            },
            {
                "name": "Classes",
                "course_statuses": {"CM1005-01": "exam prep"},
                "notes": ["Inheritance is an important concept."]
            }
        ]
    }
    with patch("builtins.input", side_effect = ["1", "2", "1", "8", "3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:
            with patch("courses_menu.topics.assign_topic_to_course", return_value = (True, "assigned")) as mock_assign:

              courses_menu.manage_courses_menu(data)

              mock_assign.assert_called_once_with(data, "Classes", "CM1035-01")


def test_manage_courses_menu_assign_topic_to_course_no_topics():
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
        ]
    }
    with patch("builtins.input", side_effect = ["1", "2", "8", "3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:
            with patch("courses_menu.topics.assign_topic_to_course") as mock_assign:
                with patch("builtins.print") as mock_print:

                    courses_menu.manage_courses_menu(data)

                    mock_assign.assert_not_called()
                    mock_print.assert_any_call("No topics available for assignment!\n")


def test_manage_courses_menu_change_topic_course_status_success():
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
        ]
    }
    with patch("builtins.input", side_effect = ["1", "3", "1", "1", "8", "3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:
            with patch("courses_menu.topics.change_topic_course_status", return_value = (True, "changed")) as mock_change_status:
                with patch("builtins.print") as mock_print:

                    courses_menu.manage_courses_menu(data)

                    mock_change_status.assert_called_once_with(data, "Recursion", "CM1035-01", "exam prep")
                    mock_print.assert_any_call("Status of topic Recursion is changed to exam prep!\n")


def test_manage_courses_menu_change_topic_course_status_no_topic_assigned():
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
        ]
    }
    with patch("builtins.input", side_effect = ["1", "3", "8", "3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:
            with patch("courses_menu.topics.change_topic_course_status") as mock_change_status:
                with patch("builtins.print") as mock_print:

                    courses_menu.manage_courses_menu(data)

                    mock_change_status.assert_not_called()
                    mock_print.assert_any_call("No topics assigned to this course!\n")


def test_manage_courses_menu_unassign_topic_success():
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
        ]
    }
    with patch("builtins.input", side_effect = ["1", "4", "1", "8", "3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:
            with patch("courses_menu.topics.unassign_topic_from_course", return_value = (True, "unassigned")) as mock_unassign:
                with patch("builtins.print") as mock_print:

                    courses_menu.manage_courses_menu(data)

                    mock_unassign.assert_called_once_with(data, "Recursion", "CM1035-01")
                    mock_print.assert_any_call("Topic Recursion has been unassigned from course CM1035-01 - Algorithms and Data Structures I.\n")


def test_manage_courses_menu_unassign_topic_from_course_no_topic_assigned():
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
        ]
    }
    with patch("builtins.input", side_effect = ["1", "4", "8", "3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:
            with patch("courses_menu.topics.unassign_topic_from_course") as mock_unassign:
                with patch("builtins.print") as mock_print:

                    courses_menu.manage_courses_menu(data)

                    mock_unassign.assert_not_called()
                    mock_print.assert_any_call("No topics assigned to this course!\n")


def test_manage_courses_menu_edit_course_success():
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
        ]
    }
    with patch("builtins.input", side_effect = ["1", "5", "1", "Introduction to Programming I", "8", "3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:
            with patch("courses_menu.courses.edit_course", return_value = (True, "updated")) as mock_edit_course:
                with patch("builtins.print") as mock_print:

                    courses_menu.manage_courses_menu(data)

                    mock_edit_course.assert_called_once_with(data, "CM1035-01", "name", "Introduction to Programming I")
                    mock_print.assert_any_call("Course CM1035-01 name has been changed to Introduction to Programming I.\n")


def test_manage_courses_menu_edit_course_empty_field():
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
        ]
    }
    with patch("builtins.input", side_effect = ["1", "5", "1", " ", "8", "3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:
            with patch("courses_menu.courses.edit_course", return_value = (False, "empty field")) as mock_edit_course:
                with patch("builtins.print") as mock_print:

                    courses_menu.manage_courses_menu(data)

                    mock_edit_course.assert_called_once_with(data, "CM1035-01", "name", " ")
                    mock_print.assert_any_call("New value cannot be empty!\n")


@pytest.mark.parametrize("current_status, new_status", [("active", "finished"), ("finished", "active")])
def test_manage_courses_menu_change_course_status_success(current_status, new_status):
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": current_status
            }
        ],
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {"CM1035-01": "learning"},
                "notes": ["base case", "recursive case"]
            }
        ]
    }
    with patch("builtins.input", side_effect = ["1", "6", "8", "3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:
            with patch("courses_menu.courses.change_course_status", return_value = (True, "updated")) as mock_change_course_status:
                with patch("builtins.print") as mock_print:

                    courses_menu.manage_courses_menu(data)

                    mock_change_course_status.assert_called_once_with(data, "CM1035-01", new_status)
                    mock_print.assert_any_call(f"Course CM1035-01 - Algorithms and Data Structures I has been changed to {new_status}.\n")


def test_manage_courses_menu_delete_course_success():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "finished"
            }
        ],
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {},
                "notes": ["base case", "recursive case"]
            }
        ]
    }
    with patch("builtins.input", side_effect = ["1", "7", "y", "3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:
            with patch("courses_menu.courses.delete_course", return_value = (True, "deleted")) as mock_delete:
                with patch("builtins.print") as mock_print:

                    courses_menu.manage_courses_menu(data)

                    mock_delete.assert_called_once_with(data, "CM1035-01")
                    mock_print.assert_any_call("Course CM1035-01 - Algorithms and Data Structures I has been deleted.\n")


def test_manage_courses_menu_delete_course_no_confirmation():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "finished"
            }
        ],
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {},
                "notes": ["base case", "recursive case"]
            }
        ]
    }
    with patch("builtins.input", side_effect = ["1", "7", "n", "8", "3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:
            with patch("courses_menu.courses.delete_course") as mock_delete:
                with patch("builtins.print") as mock_print:

                    courses_menu.manage_courses_menu(data)

                    mock_delete.assert_not_called()
                    mock_print.assert_any_call("Course is not deleted!\n")


def test_manage_courses_menu_delete_course_has_topics():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "finished"
            }
        ],
        "topics": [
            {
                "name": "Recursion",
                "course_statuses": {"CM1035-01": "learning"},
                "notes": ["base case", "recursive case"]
            }
        ]
    }
    with patch("builtins.input", side_effect = ["1", "7", "y", "8", "3"]):
        with patch("courses_menu.courses.show_course_card") as mock_show_card:
            with patch("courses_menu.courses.delete_course", return_value = (False, "course has topics")) as mock_delete:
                with patch("builtins.print") as mock_print:

                    courses_menu.manage_courses_menu(data)

                    mock_delete.assert_called_once_with(data, "CM1035-01")
                    mock_print.assert_any_call("This course has topics assigned, not possible to delete.\n")