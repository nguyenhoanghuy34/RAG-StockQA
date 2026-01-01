# api/chat.py

from fastapi import APIRouter
from pydantic import BaseModel

from services.faq_service import FAQService
from services.llm_service import ask_llm
from core.config import FAQ_THRESHOLD


router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    question: str
    answer: str
    source: str
    similarity: float | None = None


def build_chat_router(faq_service: FAQService):

    @router.post("/chat/response", response_model=ChatResponse)
    def chat(req: ChatRequest):
        faq_result = faq_service.find_best_match(
            user_question=req.message,
            threshold=FAQ_THRESHOLD
        )

        if faq_result:
            return {
                "question": req.message,
                "answer": faq_result["answer"],
                "source": faq_result["source"],
                "similarity": faq_result["similarity"]
            }

        llm_result = ask_llm(req.message)
        return {
            "question": req.message,
            "answer": llm_result["answer"],
            "source": llm_result["source"]
        }

    return router
