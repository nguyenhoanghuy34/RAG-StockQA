from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import FAQ_PATH, EMBEDDING_MODEL_NAME
from models.embedding_model import TextEmbeddingModel
from services.faq_service import FAQService
from api.chat import build_chat_router


app = FastAPI(title="RAG Stock QA")

# ===== CORS (BẮT BUỘC cho frontend gọi API) =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Init services =====
embedding_model = TextEmbeddingModel(EMBEDDING_MODEL_NAME)
faq_service = FAQService(FAQ_PATH, embedding_model)

# ===== Routes =====
app.include_router(build_chat_router(faq_service))
