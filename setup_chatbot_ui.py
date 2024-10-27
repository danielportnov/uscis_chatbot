from langchain_ollama.llms import OllamaLLM
import tools

def setup_chatbot():
    llm = OllamaLLM(model="llama3.1:8b")
    url = 'https://www.uscis.gov/book/export/html/68600'
    text_splits = tools.langchain_text_splitter(url)

    return llm, text_splits