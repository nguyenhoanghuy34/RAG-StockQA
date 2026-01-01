from fastapi import FastAPI

from core.config import FAQ_PATH, EMBEDDING_MODEL_NAME
from models.embedding_model import TextEmbeddingModel
from services.faq_service import FAQService
from api.chat import build_chat_router


app = FastAPI(title="RAG Stock QA")

embedding_model = TextEmbeddingModel(EMBEDDING_MODEL_NAME)
faq_service = FAQService(FAQ_PATH, embedding_model)

app.include_router(build_chat_router(faq_service))
