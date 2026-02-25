from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from app.services.orchestrator import invoke_rag, get_log_storage
from typing import List, Dict, Any

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query_id: str
    answer: str
    logs: List[Dict[str, Any]]

@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    try:
        # Run orchestrated retrieval and return answer + logs
        result = invoke_rag(request.query)
        return QueryResponse(
            query_id=result["query_id"],
            answer=result["answer"],
            logs=result["logs"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs/{query_id}", response_model=QueryResponse)
async def get_query_logs(query_id: str):
    try:
        storage = get_log_storage()
        result = storage.get_logs(query_id)
        if not result:
            raise HTTPException(status_code=404, detail="Logs not found")
        return QueryResponse(
            query_id=result["query_id"],
            answer=result["answer"],
            logs=result["logs"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
