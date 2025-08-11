import os
from app.utils.knowledge import build_metadatas
from app.utils.chunker import chunk_text
from app.services.embeddings import EmbeddingsService
from app.services.vectorstore_mongo import MongoVectorStoreService
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status

router = APIRouter(tags=["ingest"])

MAX_BYTES = 5 * 1024 * 1024


def _decode_text(raw: bytes) -> str:
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("latin-1", errors="ignore")


@router.post("/ingest", status_code=201)
async def ingest_txt(
    file: UploadFile = File(...),
    namespace: str = Form("default")
):
    filename = os.path.basename(file.filename or "")
    ext = os.path.splitext(filename)[1].lower()
    content_type = (file.content_type or "text/plain").lower()

    if ext != ".txt" and content_type != "text/plain":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Apenas arquivos .txt (text/plain) são aceitos neste endpoint.",
        )

    raw = await file.read()

    if len(raw) == 0:
        raise HTTPException(status_code=400, detail="Arquivo vazio.")

    if len(raw) > MAX_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Arquivo maior que o limite permitido ({MAX_BYTES} bytes).",
        )

    text = _decode_text(raw).replace("\r\n", "\n").replace("\r", "\n")

    chunks = chunk_text(text)

    if not chunks:
        raise HTTPException(
            status_code=400, detail="Nenhum conteúdo para ingerir.")

    embeddings = EmbeddingsService.embed(chunks)

    metas = build_metadatas(chunks, source=filename)

    MongoVectorStoreService(namespace).add(embeddings, metas)

    return {
        "message": f"Ingestão concluída com sucesso.",
    }
