import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# ----------------
# Title
# ----------------
st.title("🧠 Interview Practice Chatbot")


# Subheading / description
st.markdown(
    """
**Prepare and Practice Your Technical Interviews. Start with "hello"**.
"""
)

# Optional caption / note
st.caption(
    "⚠️ The chatbot will only ask interview-related questions. Please answer honestly to get accurate scoring."
)

# ----------------
# Load API Key
# ----------------
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ----------------
# Sidebar options
# ----------------
user_option = st.sidebar.selectbox(
    "Choose role:",
    ["Machine Learning", "Python", "Web Development", "Deep Learning",
     "Data Science", "Frontend Developer", "Backend Developer"]
)

difficulty = st.sidebar.radio(
    "Select question difficulty:",
    ["Easy", "Medium", "Hard", "Progressive"]
)

num_questions = st.sidebar.slider(
    "Number of questions:",
    min_value=5,
    max_value=20,
    value=10
)

interview_mode = st.sidebar.radio(
    "Interview Mode:",
    ["Mock (practice only)", "Real (score at end)"]
)

if st.sidebar.button("Start New Interview"):
    st.session_state.conversation = []
    st.session_state.last_option = None

# ----------------
# Dynamic role instructions
# ----------------
role_templates = {
    "Machine Learning": "- You are an ML interviewer.\n- Only ask questions related to Machine Learning.\n- Do not answer unnecessary questions.",
    "Python": "- You are a Python interviewer.\n- Only focus on Python concepts.\n- Do not answer irrelevant questions.",
    "Web Development": "- You are a Web Development interviewer.\n- Only ask questions on HTML, CSS, JS, backend basics.\n- Do not answer unrelated queries.",
    "Deep Learning": "- You are a Deep Learning interviewer.\n- Focus only on DL concepts (CNN, RNN, transformers, etc.).\n- Do not respond to unrelated questions.",
    "Data Science": "- You are a Data Science interviewer.\n- Only respond to interview-related questions.\n- Do not give unnecessary hints.",
    "Frontend Developer": "- You are a Frontend Development interviewer.\n- Only ask relevant frontend questions.\n- Minimal hints.",
    "Backend Developer": "- You are a Backend Development interviewer.\n- Only ask backend related questions.\n- Minimal feedback."
}

# Combine sidebar options into instructions
role_instructions = {
    role: f"{role_templates[role]}\n- Difficulty: {difficulty}\n- Number of questions: {num_questions}\n- Interview type: {interview_mode}"
    for role in role_templates
}

# ----------------
# Initialize session
# ----------------
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "last_option" not in st.session_state:
    st.session_state.last_option = None

# Reset conversation if role changes
if st.session_state.last_option != user_option:
    st.session_state.conversation = [
        {"role": "system", "content": role_instructions[user_option]}
    ]
    st.session_state.last_option = user_option

# ----------------
# Function to call API
# ----------------
def get_response(conversation):
    client = Groq(api_key=API_KEY)
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=conversation,
        temperature=0.7,
        max_tokens=200
    )
    return res.choices[0].message.content

# ----------------
# User input
# ----------------
user_input = st.chat_input("You:")

if user_input:  # ✅ Only call API if user types
    st.session_state.conversation.append({"role": "user", "content": user_input})
    reply = get_response(st.session_state.conversation)
    st.session_state.conversation.append({"role": "assistant", "content": reply})

# ----------------
# Display chat
# ----------------

for chat in st.session_state.conversation:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['content']}")
    elif chat["role"] == "assistant":
        st.markdown(f"**Interviewer:** {chat['content']}")