import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()
# Load API key securely
API = os.getenv("API_KEY")
client = Groq(api_key=API)

st.sidebar.title("Select Interview Type")

user_option = st.sidebar.selectbox(
    "Choose role:",
    [
        "Machine Learning",
        "Python",
        "Web Development",
        "Deep Learning",
        "Data Science",
        "Frontend Developer",
        "Backend Developer"
    ]
)

options = {
    "Machine Learning": "You are an ML interviewer. Ask questions from basic to advanced and give a final score.",
    "Python": "You are a Python interviewer. Start with basics, then medium, then advanced questions.",
    "Web Development": "You are a Web Development interviewer. Ask HTML, CSS, JS, and backend basics.",
    "Deep Learning": "You are a Deep Learning interviewer. Ask progressively harder DL questions and evaluate.",
    "Data Science": "You are a Data Science interviewer. Cover statistics, pandas, ML basics, and grade.",
    "Frontend Developer": "You are a Frontend interviewer. Ask React, JS, UI, and problem-solving questions.",
    "Backend Developer": "You are a Backend interviewer. Ask about APIs, DBs, auth, and backend logic."
}

st.title("🧠 Interviewer Chatbot")

# Reset conversation when role changes
if "last_option" not in st.session_state or st.session_state.last_option != user_option:
    st.session_state.conversation = [
        {"role": "system", "content": options[user_option]}
    ]
    st.session_state.last_option = user_option

# User input
user_input = st.chat_input("You:")

if user_input:
    st.session_state.conversation.append(
        {"role": "user", "content": user_input}
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.conversation,
        temperature=0.7,
        max_tokens=200
    )

    assistant_reply = response.choices[0].message.content
    st.session_state.conversation.append(
        {"role": "assistant", "content": assistant_reply}
    )

# Display chat
for chat in st.session_state.conversation:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['content']}")
    elif chat["role"] == "assistant":
        st.markdown(f"**Interviewer:** {chat['content']}")
