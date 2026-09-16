import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is missing")

client = OpenAI(api_key=api_key)


def build_prompt(topic, question, previous_history):
    history_text = ""
    for entry in previous_history[-5:]:
         history_text += f"""Question: {entry["question"]}\nAnswer: {entry["answer"]}\n\n"""
    prompt = f"""
    I am a first-year Computer Science student learning a new topic: {topic}.
    Previous conversation on this topic: \n{history_text}
    Please answer my question: {question}.
    Explain it at a beginner level and include one concrete example.
    Do not give me a long lecture. Answer only the question I asked."""
    return prompt

def ask_about_topic(topic,question, previous_history):
    prompt = build_prompt(topic,question, previous_history)
   
    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )


    return response.output_text