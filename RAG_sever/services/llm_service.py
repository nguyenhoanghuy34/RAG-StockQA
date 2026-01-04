import re
import pandas as pd
from sentence_transformers import SentenceTransformer
from core.config import EMBEDDING_MODEL_NAME

# HuggingFace
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

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
    text_lower = text.lower()
    if re.search(r"\d", text_lower):
        return True
    return any(k in text_lower for k in STOCK_KEYWORDS)

def _filter_stock_df(question: str) -> pd.DataFrame:
    question_upper = question.upper()
    filtered = df_stock[df_stock["symbol"].isin(SUPPORTED_SYMBOLS)]
    for symbol in SUPPORTED_SYMBOLS:
        if symbol in question_upper:
            filtered = filtered[filtered["symbol"] == symbol]
            break
    return filtered

# --- Load HF model 1 lần duy nhất (local) ---
MODEL_NAME = "TheBloke/llama-2-7b-chat-GGML"  # có thể thay model nhẹ hơn nếu máy yếu
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, legacy=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto")  # GPU nếu có, CPU fallback

def call_llm(prompt: str, max_tokens=300) -> str:
    print("Đã gọi đến đây")  # confirm hàm được gọi
    # Encode prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    # Generate output
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        temperature=0.2,
        do_sample=False  # deterministic
    )
    # Decode
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # In ra ngay trong hàm để debug
    print("Output HF local:\n", result)
    return result

# --- Hàm ask_llm HF local ---
def ask_llm(user_question: str) -> dict:
    if _is_stock_question(user_question):
        print("DEBUG: Đi vào nhánh SỐ LIỆU")  # debug nhánh stock
        stock_df = _filter_stock_df(user_question)
        if stock_df.empty:
            print("DEBUG: Không tìm thấy dữ liệu phù hợp")
            return {"answer": "Không tìm thấy dữ liệu phù hợp.", "source": "LOCAL_REPO"}
        data_context = stock_df.head(5).to_string(index=False)
        prompt = f"Dữ liệu chứng khoán:\n{data_context}\nCâu hỏi: {user_question}"
        answer = call_llm(prompt)
        return {"answer": answer, "source": "LLM+DATA"}

    print("DEBUG: Đi vào nhánh LÝ THUYẾT")  # debug nhánh lý thuyết
    prompt = f"{user_question}"
    answer = call_llm(prompt)
    return {"answer": answer, "source": "LLM"}


