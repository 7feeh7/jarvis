from pydantic import BaseModel, Field
from typing import List, Optional


# class IngestResponse(BaseModel):
#     namespace: str
#     chunks: int
#     vectors: int


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3)
    namespace: str = "default"
    top_k: int = 4
    conversation_id: str = None


class AskResponse(BaseModel):
    answer: str
    context: List[str]
    sources: List[str]
    conversation_id: str
