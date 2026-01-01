# models/embedding_model.py

from sentence_transformers import SentenceTransformer

class TextEmbeddingModel:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(texts)
