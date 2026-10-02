import ai
from unittest.mock import patch
import pytest

def test_ask_about_topic():
    conversation_entry = {
            "topic": "Recursion",
            "ai_mode": "Tutor",
            "messages": []
        }
    notes = ["note 1"]
    for i in range(1, 12, 2):
        conversation_entry["messages"].append({"role": "user", "content": f'message {i}'})
        conversation_entry["messages"].append({"role": "assistant", "content": f'message {i+1}'})
    
    with patch("ai.OpenAI") as mock_openai:
        mock_create = mock_openai.return_value.responses.create
        mock_create.return_value.output_text = "This is a test answer"
        answer = ai.ask_about_topic(conversation_entry, notes)
        expected_instructions = ai.build_instructions(conversation_entry["topic"], 
                                                      conversation_entry["ai_mode"], notes)
        
        assert answer == "This is a test answer"
        mock_create.assert_called_once_with(model="gpt-5.6-luna", 
                                            instructions=expected_instructions, 
                                            input=conversation_entry["messages"][-10:])


def test_build_instructions_socratic():
    topic_name = "Recursion"
    ai_mode = "Socratic tutor"

    instructions = ai.build_instructions(topic_name, ai_mode)

    assert topic_name in instructions
    assert "Do not give the final answer immediately" in instructions


def test_build_instructions_tutor():
    topic_name = "Recursion"
    ai_mode = "Tutor"

    instructions = ai.build_instructions(topic_name, ai_mode)

    assert topic_name in instructions
    assert "Explain concepts at a beginner level" in instructions
    assert "include one concrete example" in instructions


def test_build_instructions_debugger():
    topic_name = "Recursion"
    ai_mode = "Debugger"

    instructions = ai.build_instructions(topic_name, ai_mode)

    assert topic_name in instructions
    assert "Do not provide the corrected code immediately" in instructions
    assert "Ask one focused debugging question at a time" in instructions


def test_build_instructions_code_reviewer():
    topic_name = "Recursion"
    ai_mode = "Code reviewer"
    categories = ["Correctness/Bugs", "Readability", "Efficiency", "Edge cases", "Tests"]

    instructions = ai.build_instructions(topic_name, ai_mode)

    assert topic_name in instructions
    for entry in categories:
        assert entry in instructions
    assert "Explain the reason for every comment" in instructions
    assert "Let the student attempt each required change first" in instructions
    assert "Separate required fixes from optional improvements" in instructions
    assert "Let the student decide which optional improvements to implement" in instructions


def test_build_instructions_examiner():
    topic_name = "Recursion"
    ai_mode = "Examiner"

    instructions = ai.build_instructions(topic_name, ai_mode)
    
    assert topic_name in instructions
    assert "Ask one question at a time" in instructions
    assert " Mix open-ended and multiple-choice questions" in instructions
    assert "Do not reveal the correct answer before the student responds" in instructions


def test_build_instructions_include_notes():
    topic_name = "Recursion"
    ai_mode = "Examiner"
    notes = []
    for i in range(1,12):
        notes.append(f'Note {i}')
    
    instructions = ai.build_instructions(topic_name, ai_mode, notes=notes)

    assert "- Note 1\n" not in instructions
    assert "- Note 2\n" in instructions
    assert "- Note 11" in instructions


def test_open_api_key_does_not_exist(monkeypatch):
    conversation_entry = {
            "topic": "Recursion",
            "ai_mode": "Tutor",
            "messages": []
        }
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OPENAI_API_KEY is missing"):
        ai.ask_about_topic(conversation_entry, None)


def test_unknown_ai_mode():
    with pytest.raises(ValueError):
        ai.build_instructions("Recursion", "Unknown mode")


def test_summarize_conversation():
    conversation_entry = {
        "topic": "Recursion",
        "ai_mode": "Socratic tutor",
        "messages": [
            {"role": "user",
            "content": "What is recursion?"},
            {"role": "assistant",
            "content": "**Recursion** is when a function calls itself to solve a smaller version of the same problem."}]
    }

    with patch("ai.OpenAI") as mock_openai:
        expected_summary = "Recursion solves a problem by reducing it to smaller instances."
        mock_client = mock_openai.return_value
        mock_client.responses.create.return_value.output_text = expected_summary

        result = ai.summarize_conversation(conversation_entry)

        assert result == expected_summary
        mock_client.responses.create.assert_called_once()
        call_kwargs = mock_client.responses.create.call_args.kwargs
        assert call_kwargs["input"] == conversation_entry["messages"]


def test_summarize_conversation_empty_messages():
    conversation_entry = {
        "topic": "Recursion",
        "ai_mode": "Socratic tutor",
        "messages": []
    }
    with patch("ai.OpenAI") as mock_openai:
        result = ai.summarize_conversation(conversation_entry)

        assert result is None
        mock_openai.assert_not_called()