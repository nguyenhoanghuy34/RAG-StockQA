from models import embedding_model 

embedding_model_instance = embedding_model.TextEmbeddingModel()

def handle_message(user_message: str):
    user_embedding = embedding_model_instance.embed(user_message)
    return {
        "message": user_message,
        "embedding": user_embedding.tolist()  # chuyển numpy array sang list
    }
