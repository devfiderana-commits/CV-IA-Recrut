from typing import Optional

import numpy as np

from ..config import settings

_model = None


def _load_model() -> Optional[object]:
    global _model
    if _model is not None:
        return _model

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        return None

    try:
        _model = SentenceTransformer(settings.model_name)
        return _model
    except Exception:
        _model = None
        return None


def get_model() -> Optional[object]:
    return _load_model()


def embed_text(text: str):
    model = _load_model()
    if model is None:
        return None

    try:
        vector = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return np.asarray(vector, dtype=np.float32)
    except Exception:
        return None


def cosine_similarity(a, b) -> float:
    if a is None or b is None:
        return 0.0

    try:
        a_vec = np.asarray(a, dtype=np.float32).reshape(-1)
        b_vec = np.asarray(b, dtype=np.float32).reshape(-1)
        norm_a = np.linalg.norm(a_vec)
        norm_b = np.linalg.norm(b_vec)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        score = float(np.dot(a_vec, b_vec) / (norm_a * norm_b))
        return max(0.0, min(1.0, score))
    except Exception:
        return 0.0
