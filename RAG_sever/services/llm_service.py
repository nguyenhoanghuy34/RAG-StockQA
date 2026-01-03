import re
import pandas as pd
from sentence_transformers import SentenceTransformer
from core.config import EMBEDDING_MODEL_NAME

# --- Load embedding model (nếu muốn dùng cho similarity về sau) ---
_embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# --- Load dữ liệu chứng khoán ---
CSV_PATH = r"D:\Subject\RAG_LLM\RAG_stock\RAG-StockQA\RAG_sever\Data\Repo_data\data_realtime.csv"
df_stock = pd.read_csv(CSV_PATH)

# --- Danh sách 5 công ty được hỗ trợ ---
SUPPORTED_SYMBOLS = ["AAPL", "MSFT", "AMZN", "GOOG", "TSLA"]

# --- Từ khóa để nhận biết câu hỏi số liệu ---
STOCK_KEYWORDS = [
    "giá", "volume", "khối lượng", "EPS", "ROE", "ROA",
    "vốn hóa", "market cap", "cổ tức", "lợi nhuận", "D/E", "ROIC"
]

def _is_stock_question(text: str) -> bool:
    """
    Trả về True nếu câu hỏi liên quan đến chứng khoán số liệu
    """
    text_lower = text.lower()
    if re.search(r"\d", text_lower):
        return True
    return any(k in text_lower for k in STOCK_KEYWORDS)

def _filter_stock_df(question: str) -> pd.DataFrame:
    """
    Lọc bảng chứng khoán theo 5 công ty, dựa trên từ khóa symbol/ tên công ty
    """
    question_upper = question.upper()
    filtered = df_stock[df_stock["symbol"].isin(SUPPORTED_SYMBOLS)]
    # nếu user nhắc tên cụ thể symbol, lọc lại
    for symbol in SUPPORTED_SYMBOLS:
        if symbol in question_upper:
            filtered = filtered[filtered["symbol"] == symbol]
            break
    return filtered

def ask_llm(user_question: str) -> dict:
    """
    Nếu câu hỏi liên quan số liệu → truy xuất CSV + trả lời
    Nếu lý thuyết → trả lời mock
    """
    if _is_stock_question(user_question):
        stock_df = _filter_stock_df(user_question)
        if stock_df.empty:
            return {
                "answer": "Không tìm thấy dữ liệu cho công ty được yêu cầu.",
                "source": "LOCAL_REPO"
            }
        # chuyển top 5 dòng thành string để LLM có context
        data_context = stock_df.head(5).to_string(index=False)
        answer = f"[LLM+DATA] Dựa trên dữ liệu chứng khoán:\n{data_context}\nGiải thích: {user_question}"
        return {"answer": answer, "source": "LLM+DATA"}

    # câu hỏi lý thuyết (không cần số liệu)
    answer = f"[LLM] Giải thích ngắn gọn, mang tính học thuật: {user_question}"
    return {"answer": answer, "source": "LLM"}
