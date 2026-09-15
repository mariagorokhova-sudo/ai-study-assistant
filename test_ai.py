import ai
from unittest.mock import patch

def test_ask_about_topic():
    with patch.object(ai.client.responses, "create") as mock_create:
        mock_create.return_value.output_text = "This is a test answer"
        answer = ai.ask_about_topic("recursion", "why do you need a base case?")
        expected_prompt = ai.build_prompt("recursion", "why do you need a base case?")
        
        assert answer == "This is a test answer"
        mock_create.assert_called_once_with(model="gpt-5.6-luna", input=expected_prompt)

def test_build_prompt():
    prompt = ai.build_prompt("recursion", "why do you need a base case?")
    
    assert "recursion" in prompt
    assert "why do you need a base case?" in prompt
    assert "Answer only the question I asked" in prompt