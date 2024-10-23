#non_rag_module.py
import time
import streamlit as st
from models import init_models_non_rag
import psutil

def handle_non_rag_mode():
    if ('chat_engine' not in st.session_state or 
        'current_mode' not in st.session_state or 
        st.session_state['current_mode'] != 'non-rag'):
        st.session_state['chat_engine'] = init_models_non_rag()
        st.session_state['current_mode'] = 'non-rag'

def generate_non_rag_response(prompt):
    with st.chat_message('user'):
        st.markdown(prompt)

    # Start timing and resource monitoring
    start_time = time.time()
    start_cpu = psutil.cpu_percent()
    start_memory = psutil.virtual_memory().percent

    # Fetch context for multi-turn conversation
    context = "\n".join([msg['content'] for msg in st.session_state.messages if msg['role'] == 'assistant'])

    # Generate response
    response = st.session_state['chat_engine'](prompt, context)

    # End timing and resource monitoring
    end_time = time.time()
    end_cpu = psutil.cpu_percent()
    end_memory = psutil.virtual_memory().percent
    response_time = end_time - start_time
    cpu_usage = end_cpu - start_cpu
    memory_usage = end_memory - start_memory

    with st.chat_message('assistant'):
        st.markdown(response)

    # Log response time and resource usage
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    st.session_state.messages.append({'role': 'assistant', 'content': response})
    st.sidebar.write(f"Response Time (Non-RAG): {response_time:.2f} seconds")
    st.sidebar.write(f"CPU Usage (Non-RAG): {cpu_usage:.2f}%")
    st.sidebar.write(f"Memory Usage (Non-RAG): {memory_usage:.2f}%")
