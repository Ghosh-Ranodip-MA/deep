import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import settings


class EmbeddingModel:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = SentenceTransformer(settings.EMBEDDING_MODEL)
        return cls._instance


def compute_embedding(text: str) -> np.ndarray:
    if not text:
        return np.zeros(384, dtype=np.float32)
    model = EmbeddingModel.get_instance()
    return model.encode(text, convert_to_numpy=True).astype(np.float32)


def compute_similarity(text1: str, text2: str) -> float:
    if not text1 or not text2:
        return 0.0
    model = EmbeddingModel.get_instance()
    embeddings = model.encode([text1, text2])
    sim = np.dot(embeddings[0], embeddings[1]) / (
        np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]) + 1e-8
    )
    return float(max(0.0, sim))


def embedding_to_bytes(vec: np.ndarray) -> bytes:
    return vec.astype(np.float32).tobytes()


def bytes_to_embedding(data: bytes) -> np.ndarray:
    return np.frombuffer(data, dtype=np.float32)


def cosine_similarity_batch(query_vec, paper_vecs):
    if not paper_vecs:
        return []
    matrix = np.stack(paper_vecs)
    query_norm = query_vec / (np.linalg.norm(query_vec) + 1e-8)
    paper_norms = matrix / (np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-8)
    sims = np.dot(paper_norms, query_norm)
    return [float(max(0.0, s)) for s in sims]
