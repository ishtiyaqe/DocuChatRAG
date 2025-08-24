import faiss
import json
import os
import numpy as np
from .embeddings import embed_texts


class VectorIndex:
    def __init__(self, index_path: str, meta_path: str):
        self.index_path = index_path
        self.meta_path = meta_path
        self.index = None
        self.meta = []

    def build(self, chunks: list[str]):
        """Build a new FAISS index from text chunks."""
        embs = embed_texts(chunks)  # Should return a numpy array of shape (n, d)
        d = embs.shape[1]
        self.index = faiss.IndexFlatIP(d)  # Inner product (cosine-like)
        self.index.add(embs)
        self.meta = chunks
        self.save()

    def save(self):
        """Save the FAISS index and metadata."""
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, 'w', encoding='utf-8') as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)

    def load(self):
        """Load the FAISS index and metadata."""
        self.index = faiss.read_index(self.index_path)
        with open(self.meta_path, 'r', encoding='utf-8') as f:
            self.meta = json.load(f)
        return self

    def search(self, query: str, k: int = 5):
        """Search for the top-k most similar chunks to the query."""
        q_emb = embed_texts([query])  # Shape: (1, d)
        D, I = self.index.search(q_emb, k)
        hits = []
        for idx, score in zip(I[0], D[0]):
            if idx == -1:
                continue
            hits.append({"chunk": self.meta[idx], "score": float(score)})
        return hits
