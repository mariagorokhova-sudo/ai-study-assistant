import storage
import conversations

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
        "history": [],
        "conversations": []
    }

    storage.save_topics(data)

    assert test_file.exists()
    
    loaded_data = storage.load_topics()
    assert loaded_data == data

def test_load_topics_when_file_does_not_exist(tmp_path, monkeypatch):
    test_file = tmp_path/"missing.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    loaded_data = storage.load_topics()

    assert loaded_data == {"topics": [], "history": [], "conversations": []}

def test_load_topics_when_exisiting_file_has_no_history_and_conversation(tmp_path, monkeypatch):
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
        "history": [],
        "conversations": []
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
        "history": [],
        "conversations": []
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
        "history": [],
        "conversations": []
    }

def test_save_new_conversation(tmp_path, monkeypatch):
    test_file = tmp_path/"test_conversations.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    data = {"topics": [], "history": [], "conversations": []}
    topic = "recursion"
    ai_mode = "socratic tutor"

    conversation_entry = conversations.create_conversation(data, topic, ai_mode)
    
    role = "user"
    content = "What is recursion?"

    conversations.add_message_to_conversation(conversation_entry, role, content)
    storage.save_topics(data)

    assert test_file.exists()
    
    loaded_data = storage.load_topics()

    assert loaded_data == {
        "topics": [], 
        "history": [], 
        "conversations": [
            {
            "topic": "recursion", 
            "ai_mode": "socratic tutor", 
            "messages": [
                {"role": "user",
                "content": "What is recursion?"}]
            }
        ]
    }








