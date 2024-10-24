# Retrieval-Augmented Generation (RAG) System with Local LLMs

This repository implements a **Retrieval-Augmented Generation (RAG)** system, utilizing **Llama3** and another local LLM. The RAG system enhances chatbot functionality by combining local document retrieval with a large language model's (LLM) generative capabilities. The interface allows users to switch between RAG and non-RAG modes to compare performance.

## Features

- **RAG Mode**: Retrieves relevant content from local documents and augments the LLM responses
- **Non-RAG Mode**: Generates responses using the LLM alone, without retrieving external data
- **Streamlit-Based UI**: Supports file uploads, conversation history, and adjustable parameters such as maximum length and temperature
- **Performance Monitoring**: Tracks response time, CPU usage, and memory usage for both modes

## Getting Started

### Prerequisites

- **Python 3.8+** is required
- Install the necessary Python packages:

```bash
pip install -r requirements.txt
```

### Running the Application

1. Clone the repository:
```bash
git clone <repo-url>
cd <repo-directory>
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Upload Files: If using RAG mode, upload documents in supported formats (.txt, .pdf, .docx) through the user interface.

## Modes of Operation

- **RAG Mode**: Retrieves information from the uploaded documents to provide context-aware responses. Enable this mode via the sidebar toggle.
- **Non-RAG Mode**: LLM generates responses without document retrieval.

## Key Parameters

- **Max Length**: Adjusts the maximum length of generated responses
- **Temperature**: Controls the randomness of LLM responses (higher values produce more varied responses)

### Supported File Types
- txt
- pdf
- docx

## File Upload and Hashing

When files are uploaded, the system calculates an MD5 hash to detect any changes. If the hash changes, the files will be reloaded to reflect the updates in RAG mode.

## Performance Monitoring

The system tracks and displays:
- **Response Time**: Duration it takes for the model to generate a response
- **CPU Usage**: Percentage of CPU used during response generation
- **Memory Usage**: Percentage of memory consumed during operation

## Project Structure

- `app.py`: Main application logic and interface
- `ui.py`: Manages the user interface and chat history.
- `config.py`: Configuration settings (model names, token limits, and system prompt)
- `models.py`: Initializes models for both RAG and non-RAG modes
- `rag_module.py`: Handles RAG-specific logic for response generation
- `non_rag_module.py`: Manages response generation in non-RAG mode
- `utils.py`: Utility functions for file handling and hashing

## Future Improvements

- Expand support for additional models and RAG-specific features
- Optimize system for larger datasets and improve response times