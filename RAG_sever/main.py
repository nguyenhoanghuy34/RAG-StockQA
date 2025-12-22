# main.py
from fastapi import FastAPI

app = FastAPI(title="RAG Stock QA API")

# Logic RAG tượng trưng luôn trong main
def get_rag_answer(question: str) -> str:
    return f"Đây là câu trả lời giả lập cho câu hỏi: '{question}'"

# API endpoint
@app.get("/rag/answer")
def answer(question: str):
    answer_text = get_rag_answer(question)
    return {"question": question, "answer": answer_text}

# Chạy server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
