import json
from Core.embedding import embed_text


class FAQRetriever:
    def __init__(self, faq_path: str):
        with open(faq_path, "r", encoding="utf-8") as f:
            self.faq_data = f.read().split("\n\n")

        self.embeddings = [embed_text(q) for q in self.faq_data]

    def search(self, query: str, threshold: float = 0.8):
        query_emb = embed_text(query)

        best_score = 0
        best_answer = None

        for faq, emb in zip(self.faq_data, self.embeddings):
            score = sum(a * b for a, b in zip(query_emb, emb))

            if score > best_score:
                best_score = score
                best_answer = faq

        if best_score >= threshold:
            return {
                "answer": best_answer,
                "score": round(best_score, 3)
            }

        return None
