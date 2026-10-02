# AI Study Assistant

The application is designed for first-year Computer Science students to help them organize their studies, keep notes on specific topics they are learning, and discuss their questions with an AI assistant.

## Features
1. Add, view, and delete study topics.
2. Change a topic's status, and add notes to or delete notes from a specific topic.
3. Discuss questions with AI in 5 different learning modes.
4. Save, browse, continue and delete previous AI conversations.
5. Use up to 10 recent conversation messages and 10 recent topic notes as AI context.
6. Summarize AI conversations and save the summaries as notes for the corresponding topics.

## AI modes
1. Tutor - immediately answers the question at a beginner level, gives a concrete example.
2. Socratic tutor - does not give the answer immediately, asks questions to guide the student towards the correct answer.
3. Debugger - reviews code for bugs and uses focused questions to help the student identify the problems and work towards a solution.
4. Code reviewer - reviews the code across five categories: Correctness/Bugs, Readability, Efficiency, Edge cases and Tests; separates required fixes from optional improvements, lets the student attempt each fix, and provides feedback without immediately rewriting the code.
5. Examiner - asks one question at a time, assesses each answer, provides feedback and adjusts the difficulty of the following questions accordingly.

## Installation
Requires Python 3.9 or later.
1. Clone the repository and open the project directory:
```bash
git clone https://github.com/mariagorokhova-sudo/ai-study-assistant.git
cd ai-study-assistant
```
2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
3. Install the required dependencies:
```bash
python -m pip install -r requirements.txt
```
4. Create a `.env` file in the project directory and add your OpenAI API key:
```env
OPENAI_API_KEY=your_api_key_here
```

Do not commit the `.env` file to Git.

## Usage
Run the application:
```bash
python main.py
```

## Tests
Run the test suite:
```bash
python -m pytest -v
```

## Project structure
- `main.py` - application entry point and main menu.
- `ai.py` - OpenAI API requests and instructions for 5 AI learning modes, and conversations summarization.
- `topics.py` - study topic creation, deletion, status management, and notes.
- `conversations.py` - conversation creation and deletion, message management, filtering, and statistics.
- `storage.py` - loading data from and saving data to the JSON file.
- `topics_menu.py`, `ai_menu.py`, and `conversations_menu.py` - command-line menus for the main application features.
- `menu_utils.py` - shared functions for displaying numbered lists and processing menu selections.
- `test_*.py` - automated tests for the application functionality.

## Data storage
Application data is stored locally in `data.json`. The file contains 2 main lists:
```json
{
    "topics": [],
    "conversations": []
}
```

Each topic contains a name, status, and a list of notes.
```json
{
    "name": "recursion",
    "status": "new",
    "notes": []
}
```

Each conversation contains a topic, an AI mode, and a list of messages:
```json
{
    "topic": "recursion",
    "ai_mode": "Socratic tutor",
    "messages": [
        {
            "role": "user",
            "content": "What is a base case?"
        },
        {
            "role": "assistant",
            "content": "What happens if the recursive function never stops?"
        }
    ]
}
```