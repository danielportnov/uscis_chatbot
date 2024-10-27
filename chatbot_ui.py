import warnings
import streamlit as st
from streamlit_chat import message
from langchain_ollama.llms import OllamaLLM
import tools
from setup_chatbot_ui import setup_chatbot

warnings.filterwarnings("ignore")

@st.cache_resource
def setup_chatbot_ui():
    return setup_chatbot()

llm, text_splits = setup_chatbot_ui()

index_name = "uscis-embeddings"
namespace = "uscis-policy-manual"

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_bot_response(query):
    ids = tools.get_document_ids_from_query(index_name, namespace, query)
    context = tools.get_context_from_document_ids(ids)
    prompt = tools.get_prompt(context, query)
    return llm.invoke(prompt)

st.title("USCIS Chatbot")

user_input = st.text_input("You:", key="user_input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_response = get_bot_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        message(msg["content"], is_user=True, key=f"user_msg_{i}")
    else:
        message(msg["content"], is_user=False, key=f"bot_msg_{i}")