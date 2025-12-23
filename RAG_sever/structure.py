from datetime import datetime

def handle_message(message: str):
    bot_msg = {
        "role": "bot",
        "text": f"Câu trả lời tượng trưng cho: '{message}'",
        "timestamp": datetime.now().isoformat()
    }
    return bot_msg
