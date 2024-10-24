from langchain.llms import Ollama
from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings

llm = Ollama(model="llama3.1:8b")

print(llm("Hello, how are you?"))