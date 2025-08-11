from app.domain.schemas import AskRequest, AskResponse
from app.services.rag import RAGPipeline
from fastapi import APIRouter

router = APIRouter(tags=["ask"])


@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    pipeline = RAGPipeline(request.namespace)

    result = await pipeline.ask(
        request.question,
        request.conversation_id,
        top_k=request.top_k
    )
    return AskResponse(**result)
