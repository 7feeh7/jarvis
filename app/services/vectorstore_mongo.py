from typing import List, Dict, Tuple
from pymongo import MongoClient, ASCENDING
import numpy as np
from ..core import config


class MongoVectorStoreService:
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.mongo_client = MongoClient(config.MONGO_URI)
        self.database = self.mongo_client[config.MONGO_DB]
        self.collection = self.database[config.MONGO_COLLECTION]
        self._ensure_indexes()

    def _ensure_indexes(self):
        self.collection.create_index(
            [("namespace", ASCENDING)], background=True)
        self.collection.create_index(
            [("namespace", ASCENDING), ("hash", ASCENDING)], background=True)
        self.collection.create_index(
            [("namespace", ASCENDING), ("source", ASCENDING)], background=True)

    def add(self, embeddings: np.ndarray, metadata_list: List[Dict]) -> None:
        if embeddings is None or len(metadata_list) == 0:
            return

        if embeddings.shape[0] != len(metadata_list):
            raise ValueError("embeddings e metadatas com tamanhos diferentes")

        documents = []

        for embedding_vector, metadata in zip(embeddings, metadata_list):
            documents.append({
                "namespace": self.namespace,
                "source": metadata.get("source", ""),
                "text": metadata.get("text", ""),
                "hash": metadata.get("hash"),
                "embedding": embedding_vector.tolist(),
            })

        if documents:
            self.collection.insert_many(documents, ordered=False)

    def search(self, query: np.ndarray, top_k: int = 4) -> List[Tuple[float, Dict]]:
        if query is None or query.shape[0] == 0:
            return []
        query_vector = query[0].tolist()
        pipeline = [
            {
                "$vectorSearch": {
                    "index": config.MONGO_VECTOR_INDEX,
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": max(50, top_k * 10),
                    "limit": top_k,
                    "filter": {"namespace": self.namespace}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "text": 1,
                    "source": 1,
                    "hash": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]

        documents = list(self.collection.aggregate(pipeline))
        search_results: List[Tuple[float, Dict]] = []

        for doc in documents:
            score = float(doc.get("score", 0.0))
            metadata = {
                "text": doc.get("text", ""),
                "source": doc.get("source", ""),
                "hash": doc.get("hash"),
            }
            search_results.append((score, metadata))
        return search_results
