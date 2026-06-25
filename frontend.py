
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="Customer Support Agent",
    page_icon="🛒"
)

st.title("🛒 E-Commerce Customer Support Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask your question...")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    try:
        response = requests.post(
            API_URL,
            json={"message": user_input}
        )

        bot_reply = response.json()["response"]

    except Exception:
        bot_reply = "Unable to connect to backend server."

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )

    st.rerun()
