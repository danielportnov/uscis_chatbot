import requests
from bs4 import BeautifulSoup
import re
import torch

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

    # remove all script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    clean_text = soup.get_text()

    # remove whitespace and newlines
    clean_text = re.sub(r'\s+', ' ', clean_text)
    clean_text = clean_text.strip()

    return clean_text

def batch_text(text, batch_size=1000):
    return [text[i:i+batch_size] for i in range(0, len(text), batch_size)]