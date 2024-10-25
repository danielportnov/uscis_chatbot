from pinecone import Pinecone, ServerlessSpec
import os
from langchain_pinecone import PineconeVectorStore
from langchain_ollama import OllamaEmbeddings

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "embedding-test"
index = pc.Index(index_name)

embeddings = OllamaEmbeddings(model="llama3.1:8b")
vector_store = PineconeVectorStore(index, embeddings)

query = "What is the capital of France?"
results = vector_store.similarity_search(query, k=3)

for result in results:
    print(result.page_content)