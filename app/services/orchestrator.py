from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.tools.llm_client import get_llm
from app.tools.qdrant_retriever import get_qdrant_vector_store
from app.tools.db_retriever import fetch_chunk_content
from app.tools.s3_fetcher import fetch_raw_file_content
from app.core.config import settings

def log_step(step_name: str, message: str, color: str = "\033[94m"):
    """Helper to print formatted logs."""
    reset = "\033[0m"
    bold = "\033[1m"
    print(f"{bold}{color}[{step_name}]{reset} {message}", flush=True)

def format_docs_with_db_and_s3(docs):
    """
    Takes documents retrieved from Qdrant, fetches the exact context from PG,
    and optionally grabs raw documents from S3.
    """
    if not docs:
        log_step("QDRANT", "No matching documents found.", color="\033[93m") # Yellow
        return "No relevant context found."
        
    log_step("QDRANT", f"Retrieved {len(docs)} potential matches.")
    
    # Get IDs from Qdrant metadata. LangChain Qdrant store puts the point ID in '_id'
    chunk_ids = [
        doc.metadata.get("chunk_id") or doc.metadata.get("_id") 
        for doc in docs 
        if doc.metadata.get("chunk_id") or doc.metadata.get("_id")
    ]
    
    # Enrich with DB content
    log_step("POSTGRES", f"Fetching content for {len(chunk_ids)} chunks...", color="\033[92m") # Green
    db_chunks = fetch_chunk_content(chunk_ids)
    log_step("POSTGRES", f"Successfully retrieved {len(db_chunks)} full text chunks.", color="\033[92m")
    
    # Build formatted context
    context_str = []
    for chunk in db_chunks:
        c_id = chunk['chunk_id']
        d_id = chunk['document_id']
        content = chunk['content']
        context_str.append(f"--- Document ID: {d_id} | Chunk ID: {c_id} ---\n{content}\n")
        
    return "\n".join(context_str)

def get_rag_chain():
    """Builds and returns the LCEL RAG chain."""
    
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
        log_step("QUERY", f"Received: {inputs}", color="\033[96m") # Cyan
        return inputs

    def log_llm_start(inputs):
        log_step("LLM", f"Generating response using {settings.LLM_PROVIDER}...", color="\033[95m") # Magenta
        return inputs

    def log_prompt(prompt_value):
        log_step("PROMPT", f"\n{prompt_value.to_string()}", color="\033[93m") # Yellow
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
