import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.memory import ChatMemoryBuffer
import os
import tempfile
import hashlib

# Environment variables
os.environ['OLLAMA_NUM_PARALLEL'] = '2'
os.environ['OLLAMA_MAX_LOADED_MODELS'] = '2'

# Function to handle file upload
def handle_file_upload(uploaded_files):
    if uploaded_files:
        temp_dir = tempfile.mkdtemp()
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
        return temp_dir
    return None

# Function to calculate a hash for the uploaded files
def get_files_hash(files):
    hash_md5 = hashlib.md5()
    for file in files:
        file_bytes = file.read()
        hash_md5.update(file_bytes)
    return hash_md5.hexdigest()

# Function to prepare generation configuration
def prepare_generation_config():
    with st.sidebar:
        st.sidebar.header("Parameters")
        max_length = st.slider('Max Length', min_value=8, max_value=4096, value=512)
        temperature = st.slider('Temperature', 0.0, 1.0, 0.7, step=0.01)

    generation_config = {
        'num_ctx': max_length,
        'temperature': temperature
    }
    return generation_config

# Function to create new conversation
def create_new_conversation():
    st.session_state.messages = [{"role": "assistant", "content": "Hello, I am your assistant here, how can I help you?"}]
    if 'chat_engine' in st.session_state:
        # Reset chat memory
        st.session_state.chat_engine._memory = ChatMemoryBuffer.from_defaults(token_limit=4000)

# Function to initialize models with RAG
@st.cache_resource
def init_models_rag():
    embed_model = OllamaEmbedding(model_name="nomic-embed-text")
    Settings.embed_model = embed_model

    llm = Ollama(
        model="llama3", 
        request_timeout=360.0,
        num_ctx=generation_config['num_ctx'],
        temperature=generation_config['temperature']
    )
    Settings.llm = llm

    documents = SimpleDirectoryReader(st.session_state['temp_dir']).load_data()
    index = VectorStoreIndex.from_documents(documents)

    memory = ChatMemoryBuffer.from_defaults(token_limit=4000)
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        memory=memory,
        system_prompt="You are a chatbot, able to have normal interactions.",
    )

    return chat_engine

# Function to initialize models without RAG
@st.cache_resource
def init_models_non_rag():
    # Initialize the base LLM model
    llm = Ollama(
        model="llama3", 
        request_timeout=360.0,
        num_ctx=generation_config['num_ctx'],
        temperature=generation_config['temperature']
    )
    
    return llm



# Streamlit application
st.title("💻 Local RAG Chatbot 🤖")
st.caption("🚀 A chatbot powered by LlamaIndex and Ollama 🦙")

# Sidebar controls
with st.sidebar:
    # Mode selection
    st.header("Chat Mode")
    is_rag_mode = st.toggle('RAG Mode 📚', value=True, help="Toggle between RAG and non-RAG mode")
    
    # Show file upload only in RAG mode
    if is_rag_mode:
        st.header("Upload Data")
        uploaded_files = st.file_uploader(
            "Upload your data files:", 
            type=["txt", "pdf", "docx"],
            accept_multiple_files=True
        )
    
    # Parameters and buttons
    st.header("Actions")
    col1, col2 = st.columns(2)
    with col1:
        st.button('New Chat', on_click=create_new_conversation)
    with col2:
        st.button('Clear History', on_click=lambda: setattr(st.session_state, 'messages', [{"role": "assistant", "content": "Hello, I am your assistant here, how can I help you?"}]))

generation_config = prepare_generation_config()

# Handle RAG mode
if is_rag_mode:
    # Initialize hash for the current uploaded files
    current_files_hash = get_files_hash(uploaded_files) if uploaded_files else None

    # Detect if files have changed and init models
    if 'files_hash' in st.session_state:
        if st.session_state['files_hash'] != current_files_hash:
            st.session_state['files_hash'] = current_files_hash
            if 'chat_engine' in st.session_state:
                del st.session_state['chat_engine']
                st.cache_resource.clear()
            if uploaded_files:
                st.session_state['temp_dir'] = handle_file_upload(uploaded_files)
                st.sidebar.success("Files uploaded successfully.")
                if 'chat_engine' not in st.session_state:
                    st.session_state['chat_engine'] = init_models_rag()
            else:
                st.sidebar.error("Please upload files for RAG mode.")
    else:
        if uploaded_files:
            st.session_state['files_hash'] = current_files_hash
            st.session_state['temp_dir'] = handle_file_upload(uploaded_files)
            st.sidebar.success("Files uploaded successfully.")
            if 'chat_engine' not in st.session_state:
                st.session_state['chat_engine'] = init_models_rag()
        else:
            st.sidebar.error("Please upload files for RAG mode.")
else:
    # Non-RAG mode initialization
    if 'chat_engine' not in st.session_state or 'current_mode' not in st.session_state or st.session_state['current_mode'] != 'non-rag':
        st.session_state['chat_engine'] = init_models_non_rag()
        st.session_state['current_mode'] = 'non-rag'

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello, I am your assistant here, how can I help you?"}]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message['role'], avatar=message.get('avatar')):
        st.markdown(message['content'])

# Display chat input field at the bottom
if prompt := st.chat_input("Ask your question:"):
    # Check if chat engine is ready
    if 'chat_engine' not in st.session_state:
        st.error("Please upload files first or switch to non-RAG mode.")
        st.stop()

    with st.chat_message('user'):
        st.markdown(prompt)

    # Generate response
    response = st.session_state['chat_engine'].stream_chat(prompt)
    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        res = ''
        for token in response.response_gen:
            res += token
            message_placeholder.markdown(res + '▌')
        message_placeholder.markdown(res)

    # Add messages to history
    st.session_state.messages.append({
        'role': 'user',
        'content': prompt,
    })
    st.session_state.messages.append({
        'role': 'assistant',
        'content': response,
    })
