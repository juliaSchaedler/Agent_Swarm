
from bs4 import BeautifulSoup
import requests

def fetch_text(url: str) -> str:
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
        tag.decompose()
    text = soup.get_text(separator='\n')
    text = '\n'.join([line.strip() for line in text.splitlines() if line.strip()])
    return text

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(' '.join(chunk))
        i += chunk_size - overlap
    return chunks
