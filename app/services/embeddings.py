from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from ..core import config


class EmbeddingsService:
    _model = None

    @classmethod
    def _load(cls):
        if cls._model is None:
            cls._model = SentenceTransformer(config.EMBEDDINGS_MODEL)
        return cls._model

    @classmethod
    def embed(cls, texts: List[str]) -> np.ndarray:
        model = cls._load()
        vecs = model.encode(texts, normalize_embeddings=True,
                            convert_to_numpy=True)
        return vecs.astype("float32")
