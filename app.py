# main.py
import streamlit as st
from ui import setup_sidebar, display_chat
from models import init_models_rag, init_models_non_rag
from utils import handle_file_upload, get_files_hash
from config import *

def main():
    st.title("💻 Local Chatbot 🤖")
    st.caption("🚀 A chatbot powered by LlamaIndex and Ollama 🦙")

    # Setup sidebar and get configurations
    is_rag_mode, uploaded_files, generation_config = setup_sidebar()

    # Handle RAG mode
    if is_rag_mode:
        current_files_hash = get_files_hash(uploaded_files) if uploaded_files else None

        if 'files_hash' not in st.session_state or st.session_state['files_hash'] != current_files_hash:
            st.session_state['files_hash'] = current_files_hash
            if 'chat_engine' in st.session_state:
                del st.session_state['chat_engine']
                st.cache_resource.clear()
            
            if uploaded_files:
                st.session_state['temp_dir'] = handle_file_upload(uploaded_files)
                st.sidebar.success("Files uploaded successfully.")
                if 'chat_engine' not in st.session_state:
                    st.session_state['chat_engine'] = init_models_rag(
                        st.session_state['temp_dir'], 
                        generation_config
                    )
            else:
                st.sidebar.error("Please upload files for RAG mode.")

    # Handle non-RAG mode
    else:
        if ('chat_engine' not in st.session_state or 
            'current_mode' not in st.session_state or 
            st.session_state['current_mode'] != 'non-rag'):
            st.session_state['chat_engine'] = init_models_non_rag()
            st.session_state['current_mode'] = 'non-rag'

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "assistant", 
                                    "content": "Hello, I'm your assistant, how can I help you?"}]

    # Handle chat interaction
    prompt = display_chat()
    if prompt:
        # Check if chat engine is ready
        if 'chat_engine' not in st.session_state:
            st.error("Please upload files first or switch to non-RAG mode.")
            st.stop()

        # Display the user's message in the chat
        with st.chat_message('user'):
            st.markdown(prompt)

        # Fetch context for multi-turn conversation
        context = "\n".join([msg['content'] for msg in st.session_state.messages if msg['role'] == 'assistant'])

        # Generate response in non-RAG mode
        if not is_rag_mode:
            response = st.session_state['chat_engine'](prompt, context)

        # Display the assistant's response in the chat
        with st.chat_message('assistant'):
            st.markdown(response)

        # Add messages to chat history
        st.session_state.messages.append({
            'role': 'user',
            'content': prompt,
        })
        st.session_state.messages.append({
            'role': 'assistant',
            'content': response,
        })

if __name__ == "__main__":
    main()