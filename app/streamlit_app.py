import requests
import streamlit as st

from streamlit_chat import message

st.title("Chat with ChatGPT")

if 'history' not in st.session_state:
    st.session_state['history'] = []


def clear_text():
    st.session_state["text"] = ""


# Start conversation
prev_qry = ""
user_input = st.text_input(
    "You", "", key='text'
)
if prev_qry != user_input:
    prev_qry = user_input
    st.session_state['history'] += [{"role": "user", "content": user_input}]

    for interaction in st.session_state['history']:
        if interaction['role'] == 'user':
            message(f"You: {interaction['content']}", is_user=True)
        else:
            message(f"ChatGPT: {interaction['content']}")

    # Send user input to server
    response = requests.post("http://chatbot_fastapi:5300/chat", json={
        'text': user_input,
        'history': st.session_state['history']
    })

    # Display server response in chat bubble
    server_response = response.json()['output']
    message(f"ChatGPT: {server_response}")
    if len(st.session_state['history']) < 15:
        st.session_state['history'] += [
            {"role": "assistant", "content": server_response},
        ]
    else:
        st.session_state['history'] += [
            {"role": "assistant", "content": server_response},
        ]
        st.session_state['history'] = st.session_state['history'][5:]

