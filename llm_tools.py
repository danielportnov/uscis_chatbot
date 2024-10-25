from langchain_ollama import OllamaEmbeddings
import asyncio
import logging
from text_tools import TextDataset
from torch.utils.data import DataLoader
import time

# Configure logging at the beginning of the file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# TODO: implement threading (thread pool executor)
embed = OllamaEmbeddings(
    model="llama3.1:8b"
)

def generate_embedding(text):
    return text, embed.embed_query(text)

async def generate_embeddings_async(dataloader):
    total_items = len(dataloader)
    vectors = []

    for batch_num, batch in enumerate(dataloader):
        logging.info(f"Processing batch {batch_num} of {total_items}")
        
        # TODO: match text with batch based on pinecone db
        start_time = time.time()
        batch_vectors = await embed.aembed_documents(batch)
        end_time = time.time()
        
        vectors.extend(batch_vectors)
        
        # Log progress
        progress = (batch_num + 1 / total_items) * 100
        logging.info(f"Embedding progress: {progress:.2f}% ({batch_num}/{total_items})")

        # Log time taken for the batch
        batch_time = end_time - start_time
        logging.info(f"Batch {batch_num} took {batch_time:.2f} seconds")

    return vectors

def generate_embeddings(batched_text):
    dataset = TextDataset(batched_text)
    dataloader = DataLoader(dataset, batch_size=20, shuffle=False)

    return asyncio.run(generate_embeddings_async(dataloader))