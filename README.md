# USCIS Chatbot

Chatbot which answers questions about the USCIS application process.

## Prerequisites

- python 3.12
- conda (or other environment manager)
- Pinecone API key in `.env` file
- Ollama installed and running locally
    - You can download it at: https://ollama.com/download.

## Setup

create a new conda environment with python 3.12
```bash
conda create -n uscis_chatbot python=3.12
```

install the dependencies
```bash
pip install -r requirements.txt
```

### Getting Ollama Running

ensure that ollama is running locally
- Add Ollama installation to applications. Open Ollama app and add `ollama` to path. 
- Can test by running `ollama` in command line. Should show:

```bash
Usage:
  ollama [command]

Available Commands:
  completion  Generate the autocompletion script for the specified shell
  help        Help about any command
  pull        Pull a model from the model registry
  run         Run a model
```

pull the ollama model
```bash
ollama pull llama3.1:8b  
```

Ollama application should now be running locally (you should see a llama icon in the top right of your screen).

### Running the Chatbot

To run the chatbot run the following command:
```bash
streamlit run chatbot_ui.py
```

## Troubleshooting

- If you get a "connection refused" error when running the chatbot, it is likely because Ollama is not running. Check that Ollama is running locally.