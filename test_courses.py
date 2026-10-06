import courses
from unittest.mock import patch
import pytest

def test_add_course_success():
    data = {"courses": []}
    with patch("courses.storage.save_data") as mock_save:
        added, reason = courses.add_course(data, 
                                        "CM1035-01", 
                                        "Algorithms and Data Structures I",
                                        "October 2026 - March 2027")

        assert added is True
        assert reason == "added"
        assert data == {
            "courses": [
                {
                    "code": "CM1035-01",
                    "name": "Algorithms and Data Structures I",
                    "session": "October 2026 - March 2027",
                    "status": "active"
                }
            ]
        }
        mock_save.assert_called_once_with(data)


def test_add_course_duplicate_code():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "October 2026 - March 2027",
                "status": "active"
            }
        ]
    }
    with patch("courses.storage.save_data") as mock_save:
        added, reason = courses.add_course(data, 
                                        "cm1035-01", 
                                        "Algorithms and Data Structures I",
                                        "October 2026 - March 2027")

        assert added is False
        assert reason == "duplicate"
        mock_save.assert_not_called()
        assert data == {
            "courses": [
                {
                    "code": "CM1035-01",
                    "name": "Algorithms and Data Structures I",
                    "session": "October 2026 - March 2027",
                    "status": "active"
                }
            ]
        }


@pytest.mark.parametrize("code, course_name, session", [(" ","Algorithms and Data Structures I", "October 2026 - March 2027"),
                                                         ("CM1035-01", " ", "October 2026 - March 2027"),
                                                         ("CM1035-01", "Algorithms and Data Structures I", " ")])
def test_add_course_empty_input(code, course_name, session):
    data = {"courses": []}
    with patch("courses.storage.save_data") as mock_save:
        added, reason = courses.add_course(data, code, course_name, session)

        assert added is False
        assert reason == "empty field"
        mock_save.assert_not_called()
        assert data == {"courses": []}


def test_add_course_normalizes_input():
    data = {"courses": []}
    with patch("courses.storage.save_data") as mock_save:
        added, reason = courses.add_course(data, 
                                        " cm1035-01 ", 
                                        " Algorithms and Data Structures I ",
                                        " October 2026 - March 2027 ")

        assert data == {
            "courses": [
                {
                    "code": "CM1035-01",
                    "name": "Algorithms and Data Structures I",
                    "session": "October 2026 - March 2027",
                    "status": "active"
                }
            ]
        }
        assert added is True
        assert reason == "added"
        mock_save.assert_called_once_with(data)


def test_list_courses_all():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "October 2026 - March 2027",
                "status": "active"
            },
            {
                "code": "FC0002",
                "name": "Statistics for Computer Science",
                "session": "January 2026 - May 2026",
                "status": "finished"
            }
        ]
    }
    result = courses.list_courses(data)

    assert result == data["courses"]


@pytest.mark.parametrize("status, expected_code", [("active", "CM1035-01"), ("finished", "FC0002")])
def test_list_courses_filtered(status, expected_code):
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "October 2026 - March 2027",
                "status": "active"
            },
            {
                "code": "FC0002",
                "name": "Statistics for Computer Science",
                "session": "January 2026 - May 2026",
                "status": "finished"
            }
        ]
    }
    result = courses.list_courses(data, status=status)

    assert len(result) == 1
    assert result[0]["code"] == expected_code


def test_edit_course_name_success():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Statistics for Computer Science",
                "session": "October 2026 - March 2027",
                "status": "active"
            }
        ]
    }
    with patch("courses.storage.save_data") as mock_save:
        updated, reason = courses.edit_course(data,
                                            "cm1035-01",
                                            "name",
                                            "Algorithms and Data Structures I")

        assert updated is True
        assert reason == "updated"
        assert data["courses"][0]["name"] == "Algorithms and Data Structures I"
        assert data["courses"][0]["code"] == "CM1035-01"
        assert data["courses"][0]["session"] == "October 2026 - March 2027"
        assert data["courses"][0]["status"] == "active"
        mock_save.assert_called_once_with(data)


def test_edit_course_session_success():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            }
        ]
    }
    with patch("courses.storage.save_data") as mock_save:
        updated, reason = courses.edit_course(data,
                                            "cm1035-01",
                                            "session",
                                            "October 2026 - March 2027")

        assert updated is True
        assert reason == "updated"
        assert data["courses"][0]["name"] == "Algorithms and Data Structures I"
        assert data["courses"][0]["code"] == "CM1035-01"
        assert data["courses"][0]["session"] == "October 2026 - March 2027"
        assert data["courses"][0]["status"] == "active"
        mock_save.assert_called_once_with(data)


def test_edit_course_not_found():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            }
        ]
    }
    with patch("courses.storage.save_data") as mock_save:
        updated, reason = courses.edit_course(data,
                                            "FC1035-01",
                                            "name",
                                            "Statistics for Computer Science")

        assert updated is False
        assert reason == "course not found"
        mock_save.assert_not_called()
        assert data["courses"][0] == {
            "code": "CM1035-01",
            "name": "Algorithms and Data Structures I",
            "session": "January 2026 - May 2026",
            "status": "active"
        }


@pytest.mark.parametrize("field_name", ["code", "status"])
def test_edit_course_invalid_field(field_name):
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            }
        ]
    }
    with patch("courses.storage.save_data") as mock_save:
        updated, reason = courses.edit_course(data,
                                            "CM1035-01",
                                            field_name,
                                            "some changes")

        assert updated is False
        assert reason == "invalid field"
        mock_save.assert_not_called()
        assert data["courses"][0] == {
            "code": "CM1035-01",
            "name": "Algorithms and Data Structures I",
            "session": "January 2026 - May 2026",
            "status": "active"
        }


def test_edit_course_empty_field():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            }
        ]
    }
    with patch("courses.storage.save_data") as mock_save:
        updated, reason = courses.edit_course(data,
                                            "CM1035-01",
                                            "name",
                                            "  ")

        assert updated is False
        assert reason == "empty field"
        mock_save.assert_not_called()
        assert data["courses"][0] == {
            "code": "CM1035-01",
            "name": "Algorithms and Data Structures I",
            "session": "January 2026 - May 2026",
            "status": "active"
        }


def test_change_course_status_success():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            }
        ]
    }
    with patch("courses.storage.save_data") as mock_save:
        updated, reason = courses.change_course_status(data, "cm1035-01", "finished")

        assert updated is True
        assert reason == "updated"
        assert data["courses"][0]["status"] == "finished"
        mock_save.assert_called_once_with(data)


def test_change_course_status_back_success():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "finished"
            }
        ]
    }
    with patch("courses.storage.save_data") as mock_save:
        updated, reason = courses.change_course_status(data, "cm1035-01", "active")

        assert updated is True
        assert reason == "updated"
        assert data["courses"][0]["status"] == "active"
        mock_save.assert_called_once_with(data)


def test_change_course_status_invalid_status():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "finished"
            }
        ]
    }
    with patch("courses.storage.save_data") as mock_save:
        updated, reason = courses.change_course_status(data, "cm1035-01", "paused")

        assert updated is False
        assert reason == "invalid status"
        assert data["courses"][0]["status"] == "finished"
        mock_save.assert_not_called()


def test_change_course_status_course_not_found():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "finished"
            }
        ]
    }
    with patch("courses.storage.save_data") as mock_save:
        updated, reason = courses.change_course_status(data, "RM1035-01", "active")

        assert updated is False
        assert reason == "course not found"
        assert data["courses"][0]["status"] == "finished"
        mock_save.assert_not_called()


@pytest.mark.parametrize("code, new_status", [(" ", "active"), ("CM1035-01", " ")])
def test_change_course_status_empty_input(code, new_status):
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "finished"
            }
        ]
    }
    with patch("courses.storage.save_data") as mock_save:
        updated, reason = courses.change_course_status(data, code, new_status)

        assert updated is False
        assert reason == "empty field"
        assert data["courses"][0]["status"] == "finished"
        mock_save.assert_not_called()


def test_delete_course_success():
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
    with patch("courses.storage.save_data") as mock_save:
        deleted, reason = courses.delete_course(data, "CM1005-01")

        assert deleted is True
        assert reason == "deleted"
        assert data["courses"] == [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            }
        ]
        mock_save.assert_called_once_with(data)


def test_delete_course_impossible_has_topic_assigned():
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
    with patch("courses.storage.save_data") as mock_save:
        deleted, reason = courses.delete_course(data, "CM1035-01")

        assert deleted is False
        assert reason == "course has topics"
        assert data["courses"] == [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            },
            {
                "code": "CM1005-01",
                "name": "Introduction to Programming I",
                "session": "January 2026 - May 2026",
                "status": "active"
            }
        ]
        mock_save.assert_not_called()


def test_delete_course_not_found():
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
    with patch("courses.storage.save_data") as mock_save:
        deleted, reason = courses.delete_course(data, "XX1035-01")

        assert deleted is False
        assert reason == "course not found"
        assert data["courses"] == [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            },
            {
                "code": "CM1005-01",
                "name": "Introduction to Programming I",
                "session": "January 2026 - May 2026",
                "status": "active"
            }
        ]
        mock_save.assert_not_called()


def test_delete_course_empty_field():
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
    with patch("courses.storage.save_data") as mock_save:
        deleted, reason = courses.delete_course(data, " ")

        assert deleted is False
        assert reason == "empty field"
        assert data["courses"] == [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            },
            {
                "code": "CM1005-01",
                "name": "Introduction to Programming I",
                "session": "January 2026 - May 2026",
                "status": "active"
            }
        ]
        mock_save.assert_not_called()


def test_show_course_card():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "October 2026 - May 2027",
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
                "notes": ["Inheritance is important concept"]
            }
        ],
        "conversations": []
    }
    with patch("builtins.print") as mock_print:
        courses.show_course_card(data, data["courses"][0])

        mock_print.assert_any_call("CM1035-01 - Algorithms and Data Structures I")
        mock_print.assert_any_call("Session: October 2026 - May 2027")
        mock_print.assert_any_call("Status: active")
        mock_print.assert_any_call("Topics: 2\n")
        mock_print.assert_any_call("learning: 1")
        mock_print.assert_any_call("exam prep: 1")
        mock_print.assert_any_call("finished: 0")


def test_show_course_card_no_topics():
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
    with patch("builtins.print") as mock_print:
        courses.show_course_card(data, data["courses"][0])

        mock_print.assert_any_call("CM1035-01 - Algorithms and Data Structures I")
        mock_print.assert_any_call("Session: October 2026 - May 2027")
        mock_print.assert_any_call("Status: active")
        mock_print.assert_any_call("Topics: 0\n")
        mock_print.assert_any_call("learning: 0")
        mock_print.assert_any_call("exam prep: 0")
        mock_print.assert_any_call("finished: 0")