import tools
from pinecone import Pinecone
import os
from langchain_ollama.llms import OllamaLLM
import warnings

warnings.filterwarnings("ignore")

llm = OllamaLLM(model="llama3.1:8b")

url = 'https://www.uscis.gov/book/export/html/68600'

# split text into documents based on heading tags (document properties: page_content, metadata)
text_splits = tools.langchain_text_splitter(url)

# load embeddings into pinecone index
index_name = "uscis-embeddings"
namespace = "uscis-policy-manual-with-text"

tools.create_pinecone_index(index_name)
# tools.load_embeddings_into_pinecone(text_splits[300:], index_name, namespace)

# vector_store = tools.get_vector_store(index_name, namespace)
# retrieval_chain = tools.get_retrieval_chain(vector_store)
# query = "What is the purpose of the USCIS policy manual?"
# answer_with_context = retrieval_chain.invoke({"input": query})