import streamlit as st
from chatbot.conversation import ConversationManager
from db.firebase_handler import save_candidate_data
from ollama.ollama_interface import query_ollama
import re

st.set_page_config(page_title="TalentScout Assistant", layout="centered")

# Initialize session state
defaults = {
    "started": False,
    "step": 0,
    "answers": {},
    "questions": [],
    "tech_stack": [],
    "completed": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

conv = ConversationManager()

st.title("🤖 TalentScout Hiring Assistant")

# Step 0: Start
if not st.session_state.started:
    if st.button("Start Interview"):
        st.session_state.started = True
        st.session_state.step = 0
        conv.handle_input("greeting", "start")
        st.write("👋 Let's get started!")

# Step 1: Collect candidate details
steps = [
    "Full Name", "Email Address", "Phone Number", "Years of Experience",
    "Desired Position(s)", "Current Location", "Tech Stack (comma-separated)"
]

if st.session_state.started and st.session_state.step < len(steps):
    current = steps[st.session_state.step]
    response = st.text_input(f"{current}:", key=current)

    if st.button("Next"):
        if response:
            key = current.lower().replace(" ", "_").replace("(", "").replace(")", "")
            value = response.strip()

            if "tech_stack" in key:
                value = [t.strip() for t in value.split(",") if t.strip()]
                st.session_state.tech_stack = value
                conv.handle_input("tech_stack", value)
            else:
                conv.handle_input(key, value)

            st.session_state.step += 1

# Step 2: Generate technical questions
elif st.session_state.step == len(steps):
    tech_stack = st.session_state.tech_stack
    conv.handle_input("tech_stack", tech_stack)

    if not tech_stack:
        st.warning("⚠️ Tech stack is empty. Cannot generate questions.")
    else:
        st.info(f"🔧 Generating questions for: {', '.join(tech_stack)}")
        questions = conv.generate_followups()

        if not questions:
            st.error("❌ No technical questions generated.")
        else:
            st.session_state.questions = questions
            st.session_state.step += 1
            st.rerun()  # Force Streamlit to show questions on rerun

# Step 3: Answer technical questions
# Step 3: Answer technical questions
elif st.session_state.step == len(steps) + 1:
    st.subheader("📋 Technical Questions")
    answers = {}
    for q in st.session_state.questions:
        answers[q] = st.text_area(q, key=q)

    if st.button("Submit Answers"):
        scored_answers = {}
        total_score = 0
        count = 0

        for question, answer in answers.items():
            if answer.strip() == "":
                continue

            prompt = (
                f"Evaluate the following answer to this technical interview question.\n\n"
                f"Question: {question}\n"
                f"Answer: {answer}\n\n"
                f"Give a score between 0 and 10 and a short explanation of the score."
            )

            evaluation = query_ollama(prompt)
            score = 0
            try:
                match = re.search(r"\b([0-9]|10)\b", evaluation)
                if match:
                    score = int(match.group(1))
            except:
                score = 0

            total_score += score
            count += 1
            scored_answers[question] = {
                "answer": answer,
                "evaluation": evaluation,
                "score": score,
            }

        average_score = round(total_score / count, 2) if count else 0

        final_data = {
            **conv.context,  # Includes name, email, phone, etc.
            "tech_stack": st.session_state.tech_stack,
            "scored_answers": scored_answers,
            "average_score": average_score,
        }

        print("Final Data Saved to DB:", final_data)  # ✅ Log for debug

        save_candidate_data(final_data)

        st.success("✅ Thank you! Your answers have been recorded.")

        # Reset for next run
        st.session_state.started = False
        st.session_state.completed = True
