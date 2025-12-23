# models/embedding_model.py
from sentence_transformers import SentenceTransformer

class TextEmbeddingModel:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            print(f"Error loading model '{model_name}': {e}")
            raise

    def embed(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        try:
            embeddings = self.model.encode(texts)
            return embeddings
        except Exception as e:
            print(f"Error embedding texts: {e}")
            raise
