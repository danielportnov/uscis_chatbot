# USCIS Chatbot

Chatbot which answers questions about the USCIS application process.

## Prerequisites

- Pinecone API key
- Ollama installed and running locally
    - You can download it [here](https://ollama.com/download).

## Setup

create a new conda environment with python 3.12
```bash
conda create -n uscis_chatbot python=3.12
```

install the dependencies
```bash
pip install -r requirements.txt
```

install ollama (if not already installed)
```bash
conda install -c conda-forge ollama
```

pull the ollama model
```bash
ollama pull llama3.1:8b  
```