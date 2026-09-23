import ai
from unittest.mock import patch

def test_ask_about_topic():
    conversation_entry = {
            "topic": "Recursion",
            "ai_mode": "Tutor",
            "messages": [{"role": "user", "content": "What is a base case?"}]
        }
    
    with patch.object(ai.client.responses, "create") as mock_create:
        mock_create.return_value.output_text = "This is a test answer"
        answer = ai.ask_about_topic(conversation_entry)
        expected_instructions = ai.build_instructions(conversation_entry["topic"], 
                                                      conversation_entry["ai_mode"])
        
        assert answer == "This is a test answer"
        mock_create.assert_called_once_with(model="gpt-5.6-luna", 
                                            instructions=expected_instructions, 
                                            input=conversation_entry["messages"])


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

