# main.py
from fastapi import FastAPI

app = FastAPI()  # Tạo app FastAPI

# Route thử nghiệm
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Route với tham số
@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}


# Chạy server trực tiếp khi dùng `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
