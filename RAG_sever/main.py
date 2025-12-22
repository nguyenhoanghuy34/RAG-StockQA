from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from RAG_sever.API_sever.rag import router as rag_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rag_router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "RAG server running"}
