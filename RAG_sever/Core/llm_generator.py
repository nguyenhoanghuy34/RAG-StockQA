import requests
from config.settings import LLM_API_URL, HF_API_TOKEN

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def generate_answer(prompt: str) -> str:
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200
        }
    }

    response = requests.post(
        LLM_API_URL,
        headers=headers,
        json=payload
    )
    response.raise_for_status()

    return response.json()[0]["generated_text"]
