import storage

def test_save_topics(tmp_path, monkeypatch):
    test_file = tmp_path/"test_topics.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": []
            }
        ],
        "history": []
    }

    storage.save_topics(data)

    assert test_file.exists()
    
    loaded_data = storage.load_topics()
    assert loaded_data == data

def test_load_topics_when_file_does_not_exist(tmp_path, monkeypatch):
    test_file = tmp_path/"missing.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    loaded_data = storage.load_topics()

    assert loaded_data == {"topics": [], "history": []}

def test_load_topics_when_exisiting_file_has_no_history(tmp_path, monkeypatch):
    test_file = tmp_path/"test_topics_wo_history.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": []
            }
        ]
    }

    storage.save_topics(data)

    assert test_file.exists()

    loaded_data = storage.load_topics()

    assert loaded_data == {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": []
            }
        ],
        "history": []
    }

def test_load_topics_converts_old_notes_to_list(tmp_path, monkeypatch):
    test_file = tmp_path/"test_topics_wo_history.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    data = {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": ""
            }
        ],
        "history": []
    }

    storage.save_topics(data)

    assert test_file.exists()

    loaded_data = storage.load_topics()

    assert loaded_data == {
        "topics": [
            {
                "name": "recursion",
                "status": "new",
                "notes": []
            }
        ],
        "history": []
    }





