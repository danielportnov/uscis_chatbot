import text_tools
from langchain_pinecone import PineconeVectorStore
from langchain_ollama import OllamaEmbeddings
from pinecone import Pinecone, ServerlessSpec
from llm_tools import generate_embedding
import os

url = 'https://www.uscis.gov/book/export/html/68600'

text_splits = text_tools.langchain_text_splitter(url)

# embeddings = OllamaEmbeddings(
#     model="llama3.1:8b"
# )

# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# index_name = "embedding-test"

# index = pc.Index(index_name)

# namespace = "uscis-policy-manual"

# document, embedding = generate_embedding(text_splits[1])

# import hashlib

# def create_document_hash(document):
#     page_content = document.page_content
#     return hashlib.sha256(page_content.encode('utf-8')).hexdigest()

# document_hash = create_document_hash(document)
# print(document_hash)

# vectors = [{"id": document_hash, "values": embedding, "metadata": document.metadata if document.metadata else {}}]

# index.upsert(vectors, namespace=namespace)