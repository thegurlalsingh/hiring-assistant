import re
from chatbot.prompt_utils import generate_tech_questions

class ConversationManager:
    def __init__(self):
        self.context = {}

    def handle_input(self, key, value):
        self.context[key] = value
        print(f"[DEBUG] Context updated: {key} = {value}")

    def generate_followups(self):
        tech_stack = self.context.get("tech_stack", [])
        prompt = (
            f"Generate at least 5 concise technical interview questions for a candidate with experience in "
            f"{', '.join(tech_stack)}. Return each question as a separate bullet point or numbered list."
        )
        response = generate_tech_questions(prompt)
        print("Raw Ollama Response:", response)

        # 1. Fix escaped newlines and unicode bullets
        response = response.replace("\\n", "\n").replace("•", "\n•")
        
        # 2. Extract lines that start with bullet, number, or question formatting
        pattern = r"(?:[-•*]|\d+[.)])\s*(.+?)(?=(?:\n[-•*\d]|$))"
        matches = re.findall(pattern, response, re.DOTALL)

        # 3. Clean up each question
        questions = []
        for m in matches:
            q = re.sub(r"\s+", " ", m.strip())
            if len(q) > 10:
                questions.append(q)

        print("Generated Questions:", questions)
        return questions
