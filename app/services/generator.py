from typing import List
from ..core import config
import httpx
import os

SYSTEM_PROMPT = """You are AI assistant. Answer using the provided context snippets when relevant. If unsure, say you don't know."""


class Generator:
    def __init__(self):
        self.backend = config.LLM_BACKEND

    async def generate(self, prompt: str, context: List[str]) -> str:
        if self.backend == "ollama":
            return await self._ollama(prompt, context)
        return await self._openai(prompt, context)

    async def _openai(self, prompt: str, context: List[str]) -> str:
        api_key = config.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "[LLM not configured: set OPENAI_API_KEY or use Ollama]"
        msgs = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n" +
                "\n---\n".join(context) + f"\n\nQuestion: {prompt}"}
        ]
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": "gpt-4o-mini",
                      "messages": msgs, "temperature": 0.2},
            )
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"].strip()

    async def _ollama(self, prompt: str, context: List[str]) -> str:
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(
                f"{config.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": config.OLLAMA_MODEL,
                    "prompt": f"{SYSTEM_PROMPT}\n\nContext:\n" + "\n---\n".join(context) + f"\n\nQuestion: {prompt}",
                    "stream": False,
                },
            )
        r.raise_for_status()
        data = r.json()
        return data.get("response", "").strip()
