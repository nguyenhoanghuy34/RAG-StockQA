from fastapi import APIRouter
from pydantic import BaseModel

from Core.rag_pipeline import answer_question

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_rag(req: QuestionRequest):
    return answer_question(req.question)
