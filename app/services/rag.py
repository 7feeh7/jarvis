from typing import Dict, List
import numpy as np
import uuid
from .embeddings import EmbeddingsService
from .vectorstore_mongo import MongoVectorStoreService
from .generator import Generator
from .memory_mongo import MemoryStore


class RAGPipeline:
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.vector_store = MongoVectorStoreService(namespace)
        self.memory_store = MemoryStore(namespace)
        self.generator = Generator()

    def _search(self, question: str, top_k: int) -> tuple[List[str], List[str]]:
        query_embedding = EmbeddingsService.embed([question])
        results = self.vector_store.search(query_embedding, top_k=top_k)
        contexts = [meta.get("text", "") for _, meta in results]
        sources = [meta.get("source", "") for _, meta in results]
        return contexts, sources

    async def ask(self, question: str, conversation_id: str, top_k: int = 4) -> Dict:
        if not conversation_id:
            conversation_id = str(uuid.uuid4())

        chat_history = self.memory_store.get(conversation_id, limit=6)
        history_text = "\n".join(
            [f"{role}: {content}" for role, content in chat_history])

        contexts, sources = self._search(question, top_k)
        if history_text:
            contexts = [f"Conversation history:\n{history_text}"] + contexts

        answer = await self.generator.generate(question, contexts)

        self.memory_store.add(conversation_id, "user", question)
        self.memory_store.add(conversation_id, "assistant", answer)

        return {
            "answer": answer,
            "context": contexts,
            "sources": sources,
            "conversation_id": conversation_id,
        }
