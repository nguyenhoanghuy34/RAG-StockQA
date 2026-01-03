import re
from sentence_transformers import SentenceTransformer
from core.config import EMBEDDING_MODEL_NAME


# load embedding model 1 lần
_embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)


def _is_numeric_question(text: str) -> bool:
    """
    Heuristic đơn giản:
    - Có số
    - Hoặc từ khóa mang tính số liệu / thống kê
    """
    numeric_keywords = [
        "bao nhiêu", "giá", "số lượng", "tỷ lệ", "phần trăm",
        "doanh thu", "lợi nhuận", "EPS", "P/E", "ROE", "ROA",
        "năm", "quý", "tháng"
    ]

    if re.search(r"\d", text):
        return True

    text_lower = text.lower()
    return any(k in text_lower for k in numeric_keywords)


def ask_llm(user_question: str) -> dict:
    # --- nhánh 1: câu hỏi số liệu ---
    if _is_numeric_question(user_question):
        return {
            "answer": "Câu hỏi này sẽ được chuyển sang truy vấn repo local (chưa triển khai).",
            "source": "LOCAL_REPO"
        }

    # --- nhánh 2: câu hỏi lý thuyết ---
    # (hiện chưa gọi LLM thật, chỉ mock)
    real_question = f"Giải thích ngắn gọn, mang tính học thuật: {user_question}"

    return {
        "answer": f"[LLM] {real_question}",
        "source": "LLM"
    }
