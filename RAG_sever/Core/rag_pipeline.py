from Core.embedding import embed_text
from Core.faq_retriever import FAQRetriever
from Core.llm_generator import generate_answer

faq = FAQRetriever("Data/FAQ_stock.txt")

def answer_question(question: str):
    faq_result = faq.search(question)

    if faq_result:
        return {
            "answer": faq_result["answer"],
            "source": "FAQ",
            "score": faq_result["score"]
        }

    llm_answer = generate_answer(
        f"Trả lời câu hỏi chứng khoán sau ngắn gọn, chính xác:\n{question}"
    )

    return {
        "answer": llm_answer,
        "source": "LLM"
    }
