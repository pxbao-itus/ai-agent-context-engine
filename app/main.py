from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(title="Context Engine RAG", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}
