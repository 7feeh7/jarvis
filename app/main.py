from .api.v1 import ingest
from fastapi import FastAPI

app = FastAPI(title="AI jarvis", version="1.0.0")

app.include_router(ingest.router, prefix="")


@app.get("/health")
def helth():
    return {"status": "ok"}
