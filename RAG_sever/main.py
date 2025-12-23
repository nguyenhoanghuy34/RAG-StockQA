from fastapi import FastAPI
from pydantic import BaseModel
from structure import handle_message

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/chat/response")
def send_message(msg: Message):
    bot_msg = handle_message(msg.message)
    return bot_msg
