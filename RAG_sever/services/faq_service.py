# services/faq_service.py

import json
from typing import List, Dict, Optional
import numpy as np

from models.embedding_model import TextEmbeddingModel


class FAQService:
    def __init__(self, faq_path: str, embedding_model: TextEmbeddingModel):
        self.embedding_model = embedding_model
        self.faq_data = self._load_and_embed_faq(faq_path)

    def _load_and_embed_faq(self, path: str) -> List[Dict]:
        """
        Load FAQ từ file JSON. Hỗ trợ cả:
        - JSON array: [ {...}, {...} ]
        - JSON Lines: {...}\n{...}\n
        """
        data = []

        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()

            # Nếu bắt đầu bằng '[' → JSON array
            if content.startswith("["):
                try:
                    items = json.loads(content)
                    for idx, item in enumerate(items, start=1):
                        q, a = item.get("question"), item.get("answer")
                        if not q or not a:
                            continue
                        embedding = self.embedding_model.embed(q)[0]
                        data.append({
                            "question": q,
                            "answer": a,
                            "embedding": embedding
                        })
                except json.JSONDecodeError as e:
                    print(f"[FAQ] Lỗi đọc JSON array: {e}")

            else:
                # Xử lý JSON Lines
                for line_number, line in enumerate(content.splitlines(), start=1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        item = json.loads(line)
                        q, a = item.get("question"), item.get("answer")
                        if not q or not a:
                            continue
                        embedding = self.embedding_model.embed(q)[0]
                        data.append({
                            "question": q,
                            "answer": a,
                            "embedding": embedding
                        })
                    except json.JSONDecodeError:
                        print(f"[FAQ] JSON lỗi dòng {line_number}")

        return data

    @staticmethod
    def _cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
        return float(np.dot(v1, v2) / (norm_v1 * norm_v2))

    def find_best_match(
        self,
        user_question: str,
        threshold: float = 0.5
    ) -> Optional[Dict]:

        user_vector = self.embedding_model.embed(user_question)[0]

        best_score = 0.0
        best_item = None

        for item in self.faq_data:
            score = self._cosine_similarity(user_vector, item["embedding"])
            if score > best_score:
                best_score = score
                best_item = item

        if best_item and best_score >= threshold:
            return {
                "answer": best_item["answer"],
                "similarity": round(best_score, 4),
                "source": "FAQ"
            }

        return None
