# Retrieval-Augmented Generation (RAG) System with Local LLMs

This repository implements a **Retrieval-Augmented Generation (RAG)** system, utilizing **Llama3** and another local LLM. The RAG system enhances chatbot functionality by combining local document retrieval with a large language model's (LLM) generative capabilities. The interface allows users to switch between RAG and non-RAG modes to compare performance.

## Features

- **RAG Mode**: Retrieves relevant content from local documents and augments the LLM responses.
- **Non-RAG Mode**: Generates responses using the LLM alone, without retrieving external data.
- **Streamlit-Based UI**: Supports file uploads, conversation history, and adjustable parameters such as maximum length and temperature.
- **Performance Monitoring**: Tracks response time, CPU usage, and memory usage for both modes.

## Getting Started

### Prerequisites

- **Python 3.8+** is required.
- Install the necessary Python packages:
  
  ```txt
  pip install -r requirements.txt

