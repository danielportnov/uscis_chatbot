import os
import logging
import hashlib
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import HTMLHeaderTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import sqlite3
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
llm = OllamaLLM(model="llama3.1:8b")
embeddings = OllamaEmbeddings(model="llama3.1:8b")

# TEXT TOOLS

# splits text into documents based on heading tags (document properties: page_content, metadata)
def langchain_text_splitter(url):
    headers_to_split_on = [
        ("h1", "Header 1"),
        ("h2", "Header 2"),
        ("h3", "Header 3"),
    ]

    html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    html_header_splits = html_splitter.split_text_from_url(url)

    return html_header_splits

# HASHING TOOLS

# creates a hash for a document's page content
def create_document_hash(document):
    page_content = document.page_content
    return hashlib.sha256(page_content.encode('utf-8')).hexdigest()

# hashes multiple documents and returns a dictionary with the hash as the key and the document as the value
def hash_documents(text_splits):
    document_hashes = {}

    for document in text_splits:
        document_hash = create_document_hash(document)
        document_hashes[document_hash] = document
    return document_hashes

# EMBEDDING TOOLS

# generates embedding for a documents page content. returns document and embedding vector
def generate_embedding(document):
    text = document.page_content
    return document, embeddings.embed_query(text)

# generates embedding for a query
def generate_query_embedding(query):
    return embeddings.embed_query(query)

# PINECONE TOOLS

# creates a pinecone index (does not check if index already exists)
def create_pinecone_index(index_name):
    pc = Pinecone(api_key=PINECONE_API_KEY)

    pc.create_index(
        name=index_name,
        dimension=4096,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ) 
    )

    print(f"Index {index_name} created")

# load embeddings into pinecone index
def load_embeddings_into_pinecone(text_splits, index_name, namespace):
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(index_name)

    for i, document in enumerate(text_splits):
        print(f"Processing document {i+1} of {len(text_splits)}")
        document_hash = create_document_hash(document)
        document, embedding = generate_embedding(document)
        vectors = [{"id": document_hash, "values": embedding, "metadata": document.metadata if document.metadata else {}}]
        index.upsert(vectors, namespace=namespace)

def get_context_from_document_ids(document_ids, db_name='hashed_text_splits.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM hashed_text_splits WHERE hash IN ({})
    '''.format(', '.join(['?'] * len(document_ids))), document_ids)
    results = cursor.fetchall()
    conn.close()
    return results

# LLM TOOLS

# returns a vector store for a pinecone index
def get_vector_store(index_name, namespace):
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(index_name)
    return PineconeVectorStore(index, embeddings, namespace=namespace)

# returns a retrieval chain for a vector store
def get_retrieval_chain(vector_store):
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    retriever = vector_store.as_retriever()
    combine_documents_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    return create_retrieval_chain(retriever, combine_documents_chain)

# returns a list of document ids from a query
def get_document_ids_from_query(index_name, namespace, query):
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(index_name)
    results = index.query(namespace=namespace, vector=generate_query_embedding(query), top_k=20, include_values=True, include_metadata=True, include_text=False)
    return [res["id"] for res in results["matches"]]

# returns a prompt for the LLM
def get_prompt(context, query):
    context_str = ''
    for c in context:
        context_str += c[1]
        context_str += " " + "METADATA: " + str(c[2]) + "\n\n"
    prompt = f"Context: {context_str}\nQuery: {query}"
    return prompt

# DATABASE TOOLS

def write_hashed_text_splits_to_db(hashed_text_splits, db_name='hashed_text_splits.db'):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create a table to store the hashed text splits
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hashed_text_splits (
        hash TEXT PRIMARY KEY,
        page_content TEXT,
        metadata TEXT
    )
    ''')

    # Insert hashed text splits into the table
    for hash_value, document in hashed_text_splits.items():
        cursor.execute('''
        INSERT OR REPLACE INTO hashed_text_splits (hash, page_content, metadata)
        VALUES (?, ?, ?)
        ''', (hash_value, document.page_content, str(document.metadata)))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()