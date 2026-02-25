from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.api.routes import router as api_router

app = FastAPI(title="Context Engine RAG", version="1.0.0")

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Also serve files at root of frontend directly for convenience
@app.get("/{file_path:path}")
async def serve_static(file_path: str):
    file_full_path = os.path.join(frontend_path, file_path)
    if os.path.exists(file_full_path) and os.path.isfile(file_full_path):
        return FileResponse(file_full_path)
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/health")
def health_check():
    return {"status": "ok"}

