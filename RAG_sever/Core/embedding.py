import requests
import numpy as np
from config.settings import EMBEDDING_API_URL, HF_API_TOKEN

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def embed_text(text: str) -> np.ndarray:
    response = requests.post(
        EMBEDDING_API_URL,
        headers=headers,
        json={"inputs": text}
    )
    response.raise_for_status()

    embedding = response.json()
    return np.array(embedding).mean(axis=0)
