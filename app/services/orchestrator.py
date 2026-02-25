from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.tools.llm_client import get_llm
from app.tools.qdrant_retriever import get_qdrant_vector_store
from app.tools.db_retriever import fetch_chunk_content
from app.tools.s3_fetcher import fetch_raw_file_content
from app.core.config import settings

from contextvars import ContextVar

# Context variable to store logs for the current request
request_logs: ContextVar[list] = ContextVar("request_logs", default=[])

def add_log(step_name: str, message: str, detail: str = ""):
    """Adds a log entry to the current request context."""
    logs = request_logs.get()
    logs.append({
        "step": step_name,
        "message": message,
        "detail": detail,
        "timestamp": "" # Will be filled by frontend or here if needed
    })
    # Also keep console logging for terminal debugging
    print(f"[{step_name}] {message}")

def format_docs_with_db_and_s3(docs):
    if not docs:
        add_log("QDRANT", "No matching documents found.")
        return "No relevant context found."
        
    # Create detail string for Qdrant log
    qdrant_detail = "\n".join([f"- Doc: {doc.metadata.get('document_id', 'unknown')} (Score: {getattr(doc, 'metadata', {}).get('score', 'N/A')})" for doc in docs])
    add_log("QDRANT", f"Retrieved {len(docs)} potential matches.", detail=qdrant_detail)
    
    chunk_ids = [
        doc.metadata.get("chunk_id") or doc.metadata.get("_id") 
        for doc in docs 
        if doc.metadata.get("chunk_id") or doc.metadata.get("_id")
    ]
    
    add_log("POSTGRES", f"Fetching content for {len(chunk_ids)} chunks.")
    db_chunks = fetch_chunk_content(chunk_ids)
    
    # Create detail string for logs
    detail = "\n".join([f"- {c['document_id']} (ID: {c['chunk_id']})" for c in db_chunks])
    add_log("POSTGRES", f"Successfully retrieved {len(db_chunks)} full text chunks.", detail=detail)
    
    context_str = []
    for chunk in db_chunks:
        c_id = chunk['chunk_id']
        d_id = chunk['document_id']
        content = chunk['content']
        context_str.append(f"--- Document ID: {d_id} | Chunk ID: {c_id} ---\n{content}\n")
        
    return "\n".join(context_str)

def get_rag_chain():
    retriever = get_qdrant_vector_store().as_retriever()
    llm = get_llm()
    
    template = """You are a helpful assistant powered by a context engine. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Do not make up an answer.

Context: 
{context}

Question: {question}

Helpful Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    def log_query(inputs):
        add_log("QUERY", f"Received query: {inputs}")
        return inputs

    def log_llm_start(inputs):
        add_log("LLM", f"Generating response using {settings.LLM_PROVIDER}...")
        return inputs

    def log_prompt(prompt_value):
        # We store the full prompt in the detail field
        add_log("PROMPT", "Prompt constructed with context.", detail=prompt_value.to_string())
        return prompt_value

    # Construct the LCEL chain
    chain = (
        RunnablePassthrough() 
        | log_query 
        | {"context": retriever | format_docs_with_db_and_s3, "question": RunnablePassthrough()}
        | log_llm_start
        | prompt
        | log_prompt
        | llm
        | StrOutputParser()
    )
    
    return chain

import uuid
from app.tools.log_db import PostgresLogStorage

def get_log_storage():
    """Factory to get the configured log storage provider."""
    provider = settings.LOG_STORAGE_PROVIDER.lower()
    if provider == "postgres":
        return PostgresLogStorage()
    # Add other providers like MongoDB, Redis here
    raise ValueError(f"Unsupported log storage provider: {provider}")

def invoke_rag(query: str):
    """Wrapper to run the chain and return both answer and logs."""
    query_id = str(uuid.uuid4())
    request_logs.set([]) # Reset logs for this request
    
    chain = get_rag_chain()
    answer = chain.invoke(query)
    
    logs = request_logs.get()
    
    # Save to persistent storage
    try:
        storage = get_log_storage()
        storage.save_logs(query_id, query, answer, logs)
        add_log("STORAGE", f"Query logs persisted with ID: {query_id}")
    except Exception as e:
        print(f"Failed to persist logs: {e}")

    return {
        "query_id": query_id,
        "answer": answer,
        "logs": logs
    }


