import topics
from unittest.mock import patch
import pytest

def test_add_topic():
    data = {"topics": []}

    with patch("topics.storage.save_data") as mock_save:
        added, reason = topics.add_topic(data, "recursion")

        assert added is True
        assert reason == "added"
        assert data["topics"] == [
            {
                "name": "recursion",
                "status": "new",
                "notes": []
            }
        ]
        mock_save.assert_called_once_with(data)


def test_add_duplicate_topic():
    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": ""
            }
        ]
    }

    with patch("topics.storage.save_data") as mock_save:
        added, reason = topics.add_topic(data, "recursion")

        assert added is False
        assert reason == "duplicate"
        assert data == {
                    "topics": [
                        {
                            "name": "recursion",
                            "status": "new",
                            "notes": ""
                        }
                    ]
                }
        mock_save.assert_not_called()


def test_add_duplicate_topic_different_case():
    data = {
        "topics": [
            {
                "name": "classes",
                "status": "new",
                "notes": ""
            }
        ]
    }

    with patch("topics.storage.save_data") as mock_save:
        added, reason = topics.add_topic(data, "Classes")

        assert added is False
        assert reason == "duplicate"
        assert data == {
                    "topics": [
                        {
                            "name": "classes",
                            "status": "new",
                            "notes": ""
                        }
                    ]
                }
        mock_save.assert_not_called()


def test_add_empty_topic():
    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": ""
            }
        ]
    }

    with patch("topics.storage.save_data") as mock_save:
        added, reason = topics.add_topic(data, "   ")

        assert added is False
        assert reason == "empty"
        assert data == {
            "topics": [
                {
                    "name": "recursion",
                    "status": "new",
                    "notes": ""
                }
            ]
        }

        mock_save.assert_not_called()


def test_delete_topic():
    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": ""
            },
            {
                "name": "git",
                "status": "new",
                "notes": ""
            }
        ]
    }

    with patch("topics.storage.save_data") as mock_save:
        deleted, reason = topics.delete_topic(data, "Recursion")

        assert deleted is True
        assert reason == "deleted"
        assert data == {
            "topics": [
                {
                    "name": "git",
                    "status": "new",
                    "notes": ""
                }
            ]
        }
        mock_save.assert_called_once_with(data)


def test_delete_topic_not_found():
    data = {
        "topics": [
            {
                "name": "git",
                "status": "new",
                "notes": ""
            }
        ]
    }

    with patch("topics.storage.save_data") as mock_save:
        deleted, reason = topics.delete_topic(data, "recursion")

        assert deleted is False
        assert reason == "not found"
        assert data == {
            "topics": [
                {
                    "name": "git",
                    "status": "new",
                    "notes": ""
                }
            ]
        }
        mock_save.assert_not_called()


def test_delete_empty_topic():
    data = {
        "topics": [
            {
                "name": "git",
                "status": "new",
                "notes": ""
            }
        ]
    }

    with patch("topics.storage.save_data") as mock_save:
        deleted, reason = topics.delete_topic(data, "  ")

        assert deleted is False
        assert reason == "empty"
        assert data == {
            "topics": [
                {
                    "name": "git",
                    "status": "new",
                    "notes": ""
                }
            ]
        }

        mock_save.assert_not_called()


def test_change_topic_status():
    with patch("topics.storage.save_data") as mock_save:
        data = {
            "topics": [
                {
                    "name": "recursion",
                    "status": "new",
                    "notes": []
                }
            ]
        }

        topic_name = "Recursion"
        new_status = " In Progress "

        topics.change_topic_status(data, topic_name, new_status)

        assert data["topics"] == [
            {
                "name": "recursion",
                "status": "in progress",
                "notes": []
            }
        ]
       
        mock_save.assert_called_once_with(data)


@pytest.mark.parametrize(
    "topic_name, new_status, reason", 
    [("recursion", "banana", "invalid status"), 
    ("graphs", "in progress", "topic not found")])
def test_change_topic_status_invalid_input(topic_name, new_status, reason):
    with patch("topics.storage.save_data") as mock_save:
        data = {
            "topics": [
                {
                    "name": "recursion",
                    "status": "new",
                    "notes": ""
                }
            ]
        }

        result, actual_reason = topics.change_topic_status(data, topic_name, new_status)

        assert result == False
        assert actual_reason == reason
        assert data["topics"] == [
            {
                "name": "recursion",
                "status": "new",
                "notes": ""
            }
        ]
        mock_save.assert_not_called()


def test_add_note_to_existing_notes():
    with patch("topics.storage.save_data") as mock_save:
        data = {
                "topics": [
                    {
                        "name": "recursion",
                        "status": "new",
                        "notes": ["Base case stops recursion"]
                    }
                ]
            }
        topic_name = "recursion"
        new_note = "Recursive case calls the function again"

        result, reason = topics.add_note(data, topic_name, new_note)

        assert result == True
        assert reason == "added"
        assert data["topics"] == [
                    {
                        "name": "recursion",
                        "status": "new",
                        "notes": ["Base case stops recursion",
                                "Recursive case calls the function again"]
                    }
                ]
        mock_save.assert_called_once_with(data)


@pytest.mark.parametrize("topic_name, new_note, reason", 
                        [("functions", "note about function", "topic not found"),
                        ("recursion", "", "empty note"),
                        (("recursion", "  ", "empty note"))])
def test_add_note_to_existing_notes_invalid_input(topic_name, new_note, reason):
    with patch("topics.storage.save_data") as mock_save:
        data = {
            "topics": [
                {
                    "name": "recursion",
                    "status": "new",
                    "notes": ["Base case stops recursion"]
                }
            ]
        }
        result, actual_reason = topics.add_note(data, topic_name, new_note)

        assert result == False
        assert actual_reason == reason
        assert data["topics"] == [
            {
                "name": "recursion",
                "status": "new",
                "notes": ["Base case stops recursion"]
            }
        ]
        mock_save.assert_not_called()


def test_topics_get_notes_for_existing_topic():
    data = {
        "topics": [
            {"name": "Recursion",
            "status": "in progress",
            "notes": [
                "Recursion is when a function calls itself.",
                "You need a base case so that a function knows where to stop"
            ]}
        ],
        "conversations": []
    }
    result = topics.get_notes(data, "recursion")

    assert result == [
            "Recursion is when a function calls itself.",
            "You need a base case so that a function knows where to stop"
            ]


def test_topics_get_notes_for_existing_topic_empty_notes():
    data = {
        "topics": [
            {
                "name": "Recursion",
                "status": "in progress",
                "notes": []
            }
        ],
        "conversations": []
    }

    result = topics.get_notes(data, "recursion")

    assert result == []


def test_topics_get_notes_for_nonexisting_topic():
    data = {
        "topics": [
            {"name": "Recursion",
            "status": "in progress",
            "notes": [
                "Recursion is when a function calls itself.",
                "You need a base case so that a function knows where to stop"
            ]}
        ],
        "conversations": []
    }
    result = topics.get_notes(data, "classes")

    assert result is None


def test_delete_note():
    data = {
        "topics": [
            {
                "name": "Recursion",
                "status": "in progress",
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("topics.storage.save_data") as mock_save:
        result, reason = topics.delete_note(data, "Recursion", 0)

        assert data == {
            "topics": [
                {
                    "name": "Recursion",
                    "status": "in progress",
                    "notes": ["recursive case"]
                }
            ],
            "conversations": []
        }
        mock_save.assert_called_once_with(data)
        assert result == True
        assert reason == "deleted"


@pytest.mark.parametrize("incorrect_index", [2, -1])
def test_delete_note_incorrect_index(incorrect_index):
    data = {
        "topics": [
            {
                "name": "Recursion",
                "status": "in progress",
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("topics.storage.save_data") as mock_save:
        result, reason = topics.delete_note(data, "Recursion", incorrect_index)

        assert data == {
            "topics": [
                {
                    "name": "Recursion",
                    "status": "in progress",
                    "notes": ["base case", "recursive case"]
                }
            ],
            "conversations": []
        }
        mock_save.assert_not_called()
        assert result == False
        assert reason == "incorrect index"


def test_delete_note_topic_not_found():
    data = {
        "topics": [
            {
                "name": "Recursion",
                "status": "in progress",
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("topics.storage.save_data") as mock_save:
        result, reason = topics.delete_note(data, "Classes", 0)

        assert data == {
            "topics": [
                {
                    "name": "Recursion",
                    "status": "in progress",
                    "notes": ["base case", "recursive case"]
                }
            ],
            "conversations": []
        }
        mock_save.assert_not_called()
        assert result is False
        assert reason == "topic not found"


def test_assign_topic_to_course_success():
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
    with patch("topics.storage.save_data") as mock_save:
        assigned, reason = topics.assign_topic_to_course(data, "Recursion", "CM1035-01")

        assert assigned is True
        assert reason == "assigned"
        assert data["topics"][0]["course_statuses"] == {"CM1035-01": "learning"}
        mock_save.assert_called_once_with(data)


def test_assign_topic_to_course_course_not_found():
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
    with patch("topics.storage.save_data") as mock_save:
        assigned, reason = topics.assign_topic_to_course(data, "Recursion", "XX1035-01")

        assert assigned is False
        assert reason == "course not found"
        assert data["topics"][0]["course_statuses"] == {}
        mock_save.assert_not_called()


def test_assign_topic_to_course_topic_not_found():
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
    with patch("topics.storage.save_data") as mock_save:
        assigned, reason = topics.assign_topic_to_course(data, "Unknown topic", "CM1035-01")

        assert assigned is False
        assert reason == "topic not found"
        assert data["topics"][0]["course_statuses"] == {}
        mock_save.assert_not_called()


def test_assign_topic_to_course_duplicate():
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
    with patch("topics.storage.save_data") as mock_save:
        assigned, reason = topics.assign_topic_to_course(data, "Recursion", "cm1035-01")

        assert assigned is False
        assert reason == "duplicate"
        assert data["topics"][0]["course_statuses"] == {"CM1035-01": "learning"}
        mock_save.assert_not_called()


def test_assign_topic_to_course_no_course_statuses_key():
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
                "status": "new",
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("topics.storage.save_data") as mock_save:
        assigned, reason = topics.assign_topic_to_course(data, "Recursion", "CM1035-01")

        assert assigned is True
        assert reason == "assigned"
        assert data["topics"][0]["course_statuses"] == {"CM1035-01": "learning"}
        mock_save.assert_called_once_with(data)


def test_assign_topic_to_many_courses():
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
                "course_statuses": {"CM1035-01": "exam prep"},
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("topics.storage.save_data") as mock_save:
        assigned, reason = topics.assign_topic_to_course(data, "Recursion", "CM1005-01")

        assert assigned is True
        assert reason == "assigned"
        assert data["topics"][0]["course_statuses"] == {"CM1035-01": "exam prep", "CM1005-01": "learning" }
        mock_save.assert_called_once_with(data)


@pytest.mark.parametrize("topic_name, course_code", [(" ", "CM1035-01"), ("Recursion", " ")])
def test_assign_topic_to_course_empty_field(topic_name, course_code):
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
    with patch("topics.storage.save_data") as mock_save:
        assigned, reason = topics.assign_topic_to_course(data, topic_name, course_code)

        assert assigned is False
        assert reason == "empty field"
        assert data["topics"][0]["course_statuses"] == {}
        mock_save.assert_not_called()


def test_change_topic_course_status_success():
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
    with patch("topics.storage.save_data") as mock_save:
        changed, reason = topics.change_topic_course_status(data, "Recursion", "CM1035-01", "exam prep")

        assert changed is True
        assert reason == "changed"
        assert data["topics"][0]["course_statuses"]["CM1035-01"] == "exam prep"
        mock_save.assert_called_once_with(data)


def test_change_topic_course_status_topic_not_assigned_to_course():
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
    with patch("topics.storage.save_data") as mock_save:
        changed, reason = topics.change_topic_course_status(data, "Recursion", "CM1035-01", "exam prep")

        assert changed is False
        assert reason == "topic not assigned"
        assert data["topics"][0]["course_statuses"] == {}
        mock_save.assert_not_called()


def test_change_topic_course_status_invalid_status():
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
    with patch("topics.storage.save_data") as mock_save:
        changed, reason = topics.change_topic_course_status(data, "Recursion", "CM1035-01", "paused")

        assert changed is False
        assert reason == "invalid status"
        assert data["topics"][0]["course_statuses"]["CM1035-01"] == "learning"
        mock_save.assert_not_called()


def test_change_topic_course_status_topic_not_found():
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
    with patch("topics.storage.save_data") as mock_save:
        changed, reason = topics.change_topic_course_status(data, "Classes", "CM1035-01", "exam prep")

        assert changed is False
        assert reason == "topic not found"
        assert data["topics"] == [
            {
                "name": "Recursion",
                "course_statuses": {"CM1035-01": "learning"},
                "notes": ["base case", "recursive case"]
            }
        ]
        mock_save.assert_not_called()


@pytest.mark.parametrize("topic_name, course_code", [(" ", "CM1035-01"), ("Recursion", " ")])
def test_change_topic_course_status_empty_field(topic_name, course_code):
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
    with patch("topics.storage.save_data") as mock_save:
        changed, reason = topics.change_topic_course_status(data, topic_name, course_code, "exam prep")

        assert changed is False
        assert reason == "empty field"
        assert data["topics"] == [
            {
                "name": "Recursion",
                "course_statuses": {"CM1035-01": "learning"},
                "notes": ["base case", "recursive case"]
            }
        ]
        mock_save.assert_not_called()


def test_unassign_topic_from_course_success():
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
                "course_statuses": {"CM1035-01": "exam prep", "CM1005-01": "learning"},
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("topics.storage.save_data") as mock_save:
        unassigned, reason = topics.unassign_topic_from_course(data, "Recursion", "CM1005-01")

        assert unassigned is True
        assert reason == "unassigned"
        assert data["topics"][0]["course_statuses"] == {"CM1035-01": "exam prep"}
        assert data["topics"][0]["notes"] == ["base case", "recursive case"]
        mock_save.assert_called_once_with(data)


def test_unassign_topic_from_course_no_course_statuses():
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
                "status": "new",
                "notes": ["base case", "recursive case"]
            }
        ],
        "conversations": []
    }
    with patch("topics.storage.save_data") as mock_save:
        unassigned, reason = topics.unassign_topic_from_course(data, "Recursion", "CM1005-01")

        assert unassigned is False
        assert reason == "topic not assigned"
        assert data["topics"][0] == {
                "name": "Recursion",
                "status": "new",
                "notes": ["base case", "recursive case"]
            }
        mock_save.assert_not_called()


def test_unassign_topic_from_course_topic_not_found():
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
    with patch("topics.storage.save_data") as mock_save:
        unassigned, reason = topics.unassign_topic_from_course(data, "Classes", "CM1005-01")

        assert unassigned is False
        assert reason == "topic not found"
        assert data["topics"] == [
            {
                "name": "Recursion",
                "course_statuses": {"CM1035-01": "learning"},
                "notes": ["base case", "recursive case"]
            }
        ]
        mock_save.assert_not_called()


@pytest.mark.parametrize("topic_name, course_code", [(" ", "CM1035-01"), ("Recursion", " ")])
def test_unassign_topic_from_course_empty_field(topic_name, course_code):
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
    with patch("topics.storage.save_data") as mock_save:
        unassigned, reason = topics.unassign_topic_from_course(data, topic_name, course_code)

        assert unassigned is False
        assert reason == "empty field"
        assert data["topics"] == [
            {
                "name": "Recursion",
                "course_statuses": {"CM1035-01": "learning"},
                "notes": ["base case", "recursive case"]
            }
        ]
        mock_save.assert_not_called()


def test_get_topics_for_course():
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
            },
            {
                "name": "Classes",
                "course_statuses": {"CM1005-01": "learning"},
                "notes": ["Inheritance is important concept"]
            }
        ],
        "conversations": []
    }
    topics_list = topics.get_topics_for_course(data, "cm1035-01")

    assert topics_list == [
        {
            "name": "Recursion",
            "course_statuses": {"CM1035-01": "learning"},
            "notes": ["base case", "recursive case"]
        }
    ]


@pytest.mark.parametrize("course_code", [" ", "XX1035-01"])
def test_get_topics_for_course_no_matches(course_code):
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
    topics_list = topics.get_topics_for_course(data, course_code)

    assert topics_list == []


def test_show_topics_for_course():
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
    with patch("builtins.print") as mock_print:
        topics.show_topics_for_course(data, "CM1035-01")

        mock_print.assert_any_call("learning:")
        mock_print.assert_any_call("1. Recursion")
        mock_print.assert_any_call("exam prep:")
        mock_print.assert_any_call("2. Classes")
        mock_print.assert_any_call("finished:")
        mock_print.assert_any_call("3. Binary trees")


def test_show_topics_for_course_no_topics_assigned():
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
                "course_statuses": {"CM1005-01": "learning"},
                "notes": ["base case", "recursive case"]
            },
            {
                "name": "Classes",
                "course_statuses": {},
                "notes": ["Inheritance is an important concept."]
            }
        ]
    }
    with patch("builtins.print") as mock_print:
        topics.show_topics_for_course(data, "CM1035-01")

        mock_print.assert_any_call("No topics assigned to this course!\n")


def test_show_topics_for_course_empty_topics():
    data = {
        "courses": [
            {
                "code": "CM1035-01",
                "name": "Algorithms and Data Structures I",
                "session": "January 2026 - May 2026",
                "status": "active"
            }
        ],
        "topics": [],
        "conversations": []
    }
    with patch("builtins.print") as mock_print:
        topics.show_topics_for_course(data, "CM1035-01")

        mock_print.assert_any_call("No topics yet!\n")