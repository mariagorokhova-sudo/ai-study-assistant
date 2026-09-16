import ai
from unittest.mock import patch

def test_ask_about_topic():
    previous_history = [
        {
            "topic": "recursion",
            "question": "what is a base case?",
            "answer": "A **base case** tells a recursive function when to stop calling itself."
        }
    ]
    with patch.object(ai.client.responses, "create") as mock_create:
        mock_create.return_value.output_text = "This is a test answer"
        answer = ai.ask_about_topic("recursion", "why do you need a base case?", previous_history)
        expected_prompt = ai.build_prompt("recursion", "why do you need a base case?", previous_history)
        
        assert answer == "This is a test answer"
        mock_create.assert_called_once_with(model="gpt-5.6-luna", input=expected_prompt)

def test_build_prompt():
    previous_history = [
        {
            "topic": "recursion",
            "question": "what is a base case?",
            "answer": "A **base case** tells a recursive function when to stop calling itself."
        }
    ]
    prompt = ai.build_prompt("recursion", "why do you need a base case?", previous_history)
    
    
    assert "recursion" in prompt
    assert "why do you need a base case?" in prompt
    assert "Answer only the question I asked" in prompt
    assert "what is a base case?" in prompt
    assert "A **base case** tells a recursive function when to stop calling itself" in prompt

def test_build_prompt_empty_history():
    previous_history = []
    prompt = ai.build_prompt("algorithms", "what is binary search?", previous_history)

    assert "algorithms" in prompt
    assert "what is binary search?" in prompt