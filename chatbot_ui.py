import streamlit as st
from streamlit_chat import message
import random

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to generate a response (placeholder)
def get_bot_response(user_input):
    responses = [
        "That's interesting! Tell me more.",
        "I see. How does that make you feel?",
        "Can you elaborate on that?",
        "Interesting perspective. What led you to think that?",
        "I understand. Is there anything else on your mind?"
    ]
    return random.choice(responses)

# Streamlit UI
st.title("Simple Chatbot")

# User input
user_input = st.text_input("You:", key="user_input")

# When user submits input
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get bot response
    bot_response = get_bot_response(user_input)
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Display chat history
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        message(msg["content"], is_user=True, key=f"user_msg_{i}")
    else:
        message(msg["content"], is_user=False, key=f"bot_msg_{i}")