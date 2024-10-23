# ui.py
import streamlit as st
from llama_index.core.memory import ChatMemoryBuffer
from config import *

# Setup sidebar controls and return configuration.
def setup_sidebar():
    with st.sidebar:
        st.header("Chat Mode")
        is_rag_mode = st.toggle(
            'RAG Mode 📚', value=True, 
            help="Toggle between RAG and non-RAG mode"
        )
        
        if is_rag_mode:
            st.header("Upload Data")
            uploaded_files = st.file_uploader(
                "Upload your data files:",
                type=SUPPORTED_FILE_TYPES,
                accept_multiple_files=True
            )
        else:
            uploaded_files = None

        st.header("Parameters")
        max_length = st.slider('Max Length', min_value=8, max_value=2048, value=DEFAULT_MAX_LENGTH)
        temperature = st.slider('Temperature', 0.0, 1.0, DEFAULT_TEMPERATURE, step=0.01)

        st.header("Actions")
        col1, col2 = st.columns(2)
        with col1:
            st.button('New Chat', on_click = create_new_conversation)
        with col2:
            st.button('Clear History', on_click = clear_chat_history)

    return is_rag_mode, uploaded_files, {'num_ctx': max_length, 'temperature': temperature}

def create_new_conversation():
    st.session_state.messages = [{"role": "assistant", "content": "Hello, I'm your assistant, how can I help you?"}]
    if 'chat_engine' in st.session_state:
        st.session_state.chat_engine._memory = ChatMemoryBuffer.from_defaults(token_limit = DEFAULT_TOKEN_LIMIT)
        
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hello, I'm your assistant, how can I help you?"}]

# Display chat messages from history and display chat input field at the bottom.
def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message['role'], avatar=message.get('avatar')):
            st.markdown(message['content'])

    return st.chat_input("Ask a question:")