import json
from typing import List, Dict, Optional
import numpy as np
from models.embedding_model import TextEmbeddingModel


class FAQService:
    def __init__(self, faq_path: str, embedding_model: TextEmbeddingModel):
        self.embedding_model = embedding_model
        self.faq_data = self._load_and_embed_faq(faq_path)

    def _load_and_embed_faq(self, path: str) -> List[Dict]:
        data = []

        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()

            # JSON array
            if content.startswith("["):
                items = json.loads(content)
                for item in items:
                    q = item.get("question")
                    a = item.get("answer")
                    if not q or not a:
                        continue

                    embedding = self.embedding_model.embed(q)[0]
                    data.append({
                        "question": q,
                        "answer": a,
                        "embedding": embedding
                    })
            else:
                raise ValueError("FAQ file không phải JSON array hợp lệ")

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
        threshold: float
    ) -> Optional[Dict]:
        """
        Trả FAQ nếu similarity >= threshold, ngược lại trả None
        """

        user_vector = self.embedding_model.embed(user_question)[0]

        best_score = 0.0
        best_item = None

        for item in self.faq_data:
            score = self._cosine_similarity(user_vector, item["embedding"])
            if score > best_score:
                best_score = score
                best_item = item

        if best_item and best_score >= threshold:
            print(
                f"[FAQ HIT] {best_item['question']} | similarity={best_score:.4f}"
            )
            return {
                "answer": best_item["answer"],
                "similarity": round(best_score, 4),
                "source": "FAQ"
            }

        print(f"[FAQ MISS] best_similarity={best_score:.4f}")
        return None
