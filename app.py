# app.py
import streamlit as st
from ui import setup_sidebar, display_chat
from config import *
from rag_module import handle_rag_mode, generate_rag_response
from non_rag_module import handle_non_rag_mode, generate_non_rag_response

def main():
    st.title("💻 Local Chatbot 🤖")
    st.caption("🚀 A chatbot powered by LlamaIndex and Ollama 🦙")

    # Setup sidebar and get configurations
    is_rag_mode, uploaded_files, generation_config = setup_sidebar()

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello, I'm your assistant, how can I help you?"}]

    # Handle RAG or non-RAG mode based on user selection
    if is_rag_mode:
        handle_rag_mode(uploaded_files, generation_config)
    else:
        handle_non_rag_mode()

    # Handle chat interaction
    prompt = display_chat()
    if prompt:
        if is_rag_mode:
            generate_rag_response(prompt)
        else:
            generate_non_rag_response(prompt)

if __name__ == "__main__":
    main()
