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

# PINECONE TOOLS

# creates a pinecone index (does not check if index already exists)
def create_pinecone_index(index_name):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

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
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(index_name)

    for i, document in enumerate(text_splits):
        print(f"Processing document {i+1} of {len(text_splits)}")
        document_hash = create_document_hash(document)
        document, embedding = generate_embedding(document)
        vectors = [{"id": document_hash, "values": embedding, "metadata": document.metadata if document.metadata else {}}]
        index.upsert(vectors, namespace=namespace)

# LLM TOOLS

# returns a vector store for a pinecone index
def get_vector_store(index_name, namespace):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(index_name)
    return PineconeVectorStore(index, embeddings, namespace=namespace)

# returns a retrieval chain for a vector store
def get_retrieval_chain(vector_store):
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    retriever = vector_store.as_retriever()
    combine_documents_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    return create_retrieval_chain(retriever, combine_documents_chain)

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






# async def generate_embeddings_async(dataloader):
#     total_items = len(dataloader)
#     vectors = []

#     for batch_num, batch in enumerate(dataloader):
#         logging.info(f"Processing batch {batch_num} of {total_items}")
        
#         # TODO: match text with batch based on pinecone db
#         start_time = time.time()
#         batch_vectors = await embed.aembed_documents(batch)
#         end_time = time.time()
        
#         vectors.extend(batch_vectors)
        
#         # Log progress
#         progress = (batch_num + 1 / total_items) * 100
#         logging.info(f"Embedding progress: {progress:.2f}% ({batch_num}/{total_items})")

#         # Log time taken for the batch
#         batch_time = end_time - start_time
#         logging.info(f"Batch {batch_num} took {batch_time:.2f} seconds")

#     return vectors

# def generate_embeddings(batched_text):
#     dataset = TextDataset(batched_text)
#     dataloader = DataLoader(dataset, batch_size=20, shuffle=False)

#     return asyncio.run(generate_embeddings_async(dataloader))

# pc.create_index(
#     name=index_name,
#     dimension=4096,
#     metric="cosine",
#     spec=ServerlessSpec(
#         cloud="aws",
#         region="us-east-1"
#     ) 
# )

# embeddings = OllamaEmbeddings(model="llama3.1:8b")
# vector_store = PineconeVectorStore(index, embeddings)

# query = "What is the capital of France?"
# results = vector_store.similarity_search(query, k=3)

# for result in results:
#     print(result.page_content)

# class TextDataset(torch.utils.data.Dataset):
#     def __init__(self, batched_text):
#         self.batched_text = batched_text

#     def __len__(self):
#         return len(self.batched_text)
    
#     def __getitem__(self, idx):
#         return self.batched_text[idx]

# embeddings = OllamaEmbeddings(
#     model="llama3.1:8b"
# )

# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# index_name = "embedding-test"

# index = pc.Index(index_name)

# namespace = "uscis-policy-manual"

# document, embedding = generate_embedding(text_splits[1])

# vectors = [{"id": document_hash, "values": embedding, "metadata": document.metadata if document.metadata else {}}]

# index.upsert(vectors, namespace=namespace)