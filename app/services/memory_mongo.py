from __future__ import annotations
from typing import List, Tuple
from pymongo import MongoClient, ASCENDING
from ..core import config


class MemoryStore:
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.client = MongoClient(config.MONGO_URI)
        self.db = self.client[config.MONGO_DB]
        self.collection = self.db[config.MONGO_MESSAGES_COLLECTION]
        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        self.collection.create_index(
            [("namespace", ASCENDING),
             ("conversation_id", ASCENDING), ("ts", ASCENDING)],
            background=True
        )

    def add(self, conversation_id: str, role: str, content: str) -> None:
        if role not in ("user", "assistant"):
            raise ValueError("role inválida: use 'user' ou 'assistant'")
        self.collection.insert_one({
            "namespace": self.namespace,
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "ts": self._now_iso(),
        })

    def get(self, conversation_id: str, limit: int = 10) -> List[Tuple[str, str]]:
        cursor = self.collection.find(
            {"namespace": self.namespace, "conversation_id": conversation_id},
            {"_id": 0, "role": 1, "content": 1}
        ).sort("ts", -1).limit(limit)
        rows = list(cursor)
        return [(r["role"], r["content"]) for r in reversed(rows)]

    def _now_iso(self) -> str:
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()
