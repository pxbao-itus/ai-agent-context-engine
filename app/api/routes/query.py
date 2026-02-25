from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from app.services.orchestrator import get_rag_chain

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

from fastapi import Depends

def get_chain():
    return get_rag_chain()

@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest, chain = Depends(get_chain)):
    try:
        # Generate answer using the LCEL RAG chain
        answer = chain.invoke(request.query)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
