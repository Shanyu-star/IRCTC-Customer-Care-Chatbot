import streamlit as st
import google.generativeai as genai

# ---- CONFIG ----

import os
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))    # Replace with your actual API key

# ---- LOAD KB ----
with open("irctc document.txt", "r") as f:
    kb = f.read()

# ---- PROMPT ----
prompt = f"""
you are IRCTC customer care excutive your job is to provide answers to the questiond asked by the customers,
you should answer them polite, if there is any question out of your kb say you did not have that info, only refer the kb and provide the response

{kb}
"""

# ---- MODEL ----
model_name_str = 'gemini-1.5-flash'
gemini_model = genai.GenerativeModel(
    model_name=model_name_str,
    system_instruction=prompt
)

# ---- STREAMLIT UI ----
st.title("IRCTC Customer Care Chatbot")

# Initialize chat session (persists across reruns)
if "chat" not in st.session_state:
    st.session_state.chat = gemini_model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask your IRCTC related question...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from Gemini
    response = st.session_state.chat.send_message(user_input)

    # Show assistant message
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    with st.chat_message("assistant"):
        st.markdown(response.text)
