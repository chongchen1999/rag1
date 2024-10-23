# models.py
import streamlit as st
import subprocess
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.memory import ChatMemoryBuffer
from config import *

def init_models_rag(temp_dir, generation_config):
    """Initialize RAG models with LlamaIndex."""
    embed_model = OllamaEmbedding(model_name=EMBEDDING_MODEL)
    Settings.embed_model = embed_model

    llm = Ollama(
        model=LLM_MODEL,
        request_timeout=LLM_TIMEOUT,
        num_ctx=generation_config['num_ctx'],
        temperature=generation_config['temperature']
    )
    Settings.llm = llm

    documents = SimpleDirectoryReader(st.session_state['temp_dir']).load_data()
    index = VectorStoreIndex.from_documents(documents)

    memory = ChatMemoryBuffer.from_defaults(token_limit=DEFAULT_TOKEN_LIMIT)
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        memory=memory,
        system_prompt=DEFAULT_SYSTEM_PROMPT,
    )

    return chat_engine

def init_models_non_rag():
    """Initialize non-RAG model using Ollama directly."""
    def run_model(prompt, context=""):
        try:
            full_prompt = context + "\n" + prompt if context else prompt
            command = ["ollama", "run", LLM_MODEL]
            process = subprocess.run(
                command,
                input=full_prompt,
                text=True,
                capture_output=True,
                check=True
            )
            return process.stdout
        except subprocess.CalledProcessError as e:
            return f"Error running Llama: {e.stderr}"
        except FileNotFoundError:
            return "Error: Ollama is not installed or not in PATH"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    return run_model