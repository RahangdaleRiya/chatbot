import os
import sys
import yaml
import json
import numpy as np
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.orm import Session

# Handle relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
shared_path = os.path.join(os.path.dirname(current_dir), '..', '..', 'shared')
if shared_path not in sys.path:
    sys.path.insert(0, shared_path)

from models import Embedding


def load_config():
    with open(os.path.join(os.path.dirname(__file__), '../../../shared/config.yml'), 'r') as f:
        return yaml.safe_load(f)


config = load_config()
embeddings = OllamaEmbeddings(
    base_url=config['ollama']['host'],
    model=config['ollama']['embedding_model']
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)

def generate_embedding(text: str) -> list:
    return embeddings.embed_query(text)


def split_text(text: str) -> list:
    return splitter.split_text(text)


def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    a_array = np.array(a)
    b_array = np.array(b)
    return np.dot(a_array, b_array) / (np.linalg.norm(a_array) * np.linalg.norm(b_array))


def search_similar(query_embedding: list, db: Session, top_k: int = 5):
    """Search for similar documents using pgvector"""
    from sqlalchemy import func
    
    all_embeddings = db.query(Embedding).all()
    similarities = []
    for emb in all_embeddings:
        # pgvector stores vectors directly
        vec = list(emb.vector) if hasattr(emb.vector, '__iter__') else emb.vector
        sim = cosine_similarity(query_embedding, vec)
        similarities.append((emb.document_id, sim))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]