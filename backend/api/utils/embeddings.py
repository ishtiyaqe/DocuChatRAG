from sentence_transformers import SentenceTransformer
import numpy as np


_MODEL = None


def get_embedder():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return _MODEL


def embed_texts(texts: list[str]) -> np.ndarray:
    model = get_embedder()
    embs = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return np.array(embs, dtype='float32')