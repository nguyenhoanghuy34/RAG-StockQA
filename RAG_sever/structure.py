from models import embedding_model

embedding_model_instance = embedding_model.TextEmbeddingModel()

# Embed toàn bộ FAQ ngay khi app chạy
FAQ_EMBEDDINGS = embedding_model.embed_faq_questions(
    file_path="FAQ_stock.txt",
    embedding_model=embedding_model_instance
)


def handle_message(user_message: str):

    result = embedding_model.find_best_faq_answer(
        user_question=user_message,
        embedding_model=embedding_model_instance,
        faq_embeddings=FAQ_EMBEDDINGS,
        threshold=0.9
    )

    if result:
        return {
            "question": user_message,
            "answer": result["answer"],
            "similarity": result["similarity"],
            "source": "FAQ_stock"
        }

    return {
        "question": user_message,
        "answer": "Xin lỗi, tôi chưa tìm thấy câu trả lời phù hợp trong FAQ.",
        "source": "fallback"
    }
