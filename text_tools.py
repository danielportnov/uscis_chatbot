import requests
from bs4 import BeautifulSoup
import torch
from langchain_text_splitters import HTMLHeaderTextSplitter

class TextDataset(torch.utils.data.Dataset):
    def __init__(self, batched_text):
        self.batched_text = batched_text

    def __len__(self):
        return len(self.batched_text)
    
    def __getitem__(self, idx):
        return self.batched_text[idx]

def get_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    content = {}

    def get_text_after_header(header_tag):
        text = []
        for sibling in header_tag.find_next_siblings():
            if sibling.name and sibling.name.startswith('h'):  # Stop at the next header (h1, h2, etc.)
                break
            text.append(sibling.get_text())
        return " ".join(text)

    for header in soup.find_all(['h1', 'h2', 'h3']):
        header_text = header.get_text()
        content[header_text] = get_text_after_header(header)

    return content

def batch_text(text, batch_size=1000):
    return [text[i:i+batch_size] for i in range(0, len(text), batch_size)]

def langchain_text_splitter(url):
    headers_to_split_on = [
        ("h1", "Header 1"),
        ("h2", "Header 2"),
        ("h3", "Header 3"),
    ]

    html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    html_header_splits = html_splitter.split_text_from_url(url)

    return html_header_splits