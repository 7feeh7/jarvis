import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "all-MiniLM-L6-v2")
LLM_BACKEND = os.getenv("LLM_BACKEND", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
MONGO_VECTOR_INDEX = os.getenv("MONGO_VECTOR_INDEX")
