import re
import pandas as pd
from sentence_transformers import SentenceTransformer
from core.config import EMBEDDING_MODEL_NAME

# --- Load embedding model (nếu muốn dùng cho similarity sau này) ---
_embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# --- Load dữ liệu chứng khoán ---
CSV_PATH = r"D:\Subject\RAG_LLM\RAG_stock\RAG-StockQA\RAG_sever\Data\Repo_data\data_realtime.csv"
df_stock = pd.read_csv(CSV_PATH)

# --- Danh sách các công ty được hỗ trợ ---
SUPPORTED_SYMBOLS = ["AAPL", "MSFT", "AMZN", "GOOG", "TSLA"]

# --- Từ khóa để nhận biết câu hỏi về số liệu ---
STOCK_KEYWORDS = [
    "giá", "volume", "khối lượng", "EPS", "ROE", "ROA",
    "vốn hóa", "market cap", "cổ tức", "lợi nhuận", "D/E", "ROIC"
]

def _is_stock_question(text: str) -> bool:
    """
    Kiểm tra xem câu hỏi có liên quan đến số liệu chứng khoán không.
    Nếu có số hoặc chứa từ khóa, trả về True.
    """
    text_lower = text.lower()
    if re.search(r"\d", text_lower):
        return True
    return any(k in text_lower for k in STOCK_KEYWORDS)

def _filter_stock_df(question: str) -> pd.DataFrame:
    """
    Lọc dữ liệu chứng khoán theo các symbol được hỗ trợ.
    Nếu trong câu hỏi có tên symbol, chỉ lấy dữ liệu của symbol đó.
    """
    question_upper = question.upper()
    filtered = df_stock[df_stock["symbol"].isin(SUPPORTED_SYMBOLS)]
    for symbol in SUPPORTED_SYMBOLS:
        if symbol in question_upper:
            filtered = filtered[filtered["symbol"] == symbol]
            break
    return filtered

# --- Load Llama 2 GGUF bằng ctransformers ---
from ctransformers import AutoModelForCausalLM

# Nếu có GPU Nvidia, set gpu_layers > 0. CPU: set gpu_layers=0
llm = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Llama-2-7b-Chat-GGUF",  # Repo online
    model_file="llama-2-7b-chat.Q4_K_M.gguf",  # Phiên bản local
    model_type="llama",
    gpu_layers=0  # set 0 nếu không có GPU
)

# --- Hàm gọi LLM ---
def call_llm(prompt: str, max_new_tokens=300) -> str:
    """
    Gọi mô hình LLM với prompt.
    """
    print("Đã gọi đến LLM")
    result = llm(prompt, max_new_tokens=max_new_tokens)
    print("Output LLM:\n", result)
    return result

# --- Hàm ask_llm tích hợp stock + lý thuyết ---
def ask_llm(user_question: str) -> dict:
    """
    Xử lý câu hỏi: nếu là câu hỏi về số liệu chứng khoán, 
    trích dữ liệu phù hợp và gọi LLM. 
    Nếu là câu hỏi lý thuyết, gọi LLM trực tiếp.
    """
    if _is_stock_question(user_question):
        print("DEBUG: Đi vào nhánh SỐ LIỆU")
        stock_df = _filter_stock_df(user_question)
        if stock_df.empty:
            print("DEBUG: Không tìm thấy dữ liệu phù hợp")
            return {"answer": "Không tìm thấy dữ liệu phù hợp.", "source": "LOCAL_REPO"}
        data_context = stock_df.head(5).to_string(index=False)
        prompt = f"Dữ liệu chứng khoán:\n{data_context}\nCâu hỏi: {user_question}"
        answer = call_llm(prompt)
        return {"answer": answer, "source": "LLM+DATA"}

    print("DEBUG: Đi vào nhánh LÝ THUYẾT")
    prompt = f"{user_question}"
    answer = call_llm(prompt)
    return {"answer": answer, "source": "LLM"}

# --- Test nhanh ---
if __name__ == "__main__":
    while True:
        q = input("Bạn hỏi: ")
        if q.lower() in ["exit", "thoát"]:
            break
        res = ask_llm(q)
        print("AI trả lời:", res["answer"])
