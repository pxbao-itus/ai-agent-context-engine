from fastapi import APIRouter
from app.api.routes import query

router = APIRouter()

router.include_router(query.router, tags=["query"])

