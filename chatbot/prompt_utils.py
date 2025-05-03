# chatbot/prompt_utils.py
from ollama.ollama_interface import query_ollama

def generate_tech_questions(prompt: str) -> str:
    return query_ollama(prompt)
