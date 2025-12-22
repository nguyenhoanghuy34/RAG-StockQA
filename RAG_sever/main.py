from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()

chat_history = {}  # lưu tạm theo user_id

class Message(BaseModel):
    user_id: str
    message: str

@app.post("/chat/send")
def send_message(msg: Message):
    user_msg = {"role": "user", "text": msg.message, "timestamp": datetime.now().isoformat()}
    bot_msg = {"role": "bot", "text": f"Câu trả lời tượng trưng cho: '{msg.message}'", "timestamp": datetime.now().isoformat()}
    
    chat_history.setdefault(msg.user_id, []).extend([user_msg, bot_msg])
    
    return bot_msg

@app.get("/chat/history/{user_id}")
def get_history(user_id: str):
    return chat_history.get(user_id, [])
