from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.tools.llm_client import get_llm
from app.tools.qdrant_retriever import get_qdrant_vector_store
from app.tools.db_retriever import fetch_chunk_content
from app.tools.s3_fetcher import fetch_raw_file_content

def format_docs_with_db_and_s3(docs):
    """
    Takes documents retrieved from Qdrant, fetches the exact context from PG,
    and optionally grabs raw documents from S3.
    """
    if not docs:
        return "No relevant context found."
        
    # Get IDs from Qdrant metadata
    chunk_ids = [doc.metadata.get("chunk_id") for doc in docs if doc.metadata.get("chunk_id")]
    
    # Enrich with DB content
    db_chunks = fetch_chunk_content(chunk_ids)
    
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
    
    # Initialize components
    # We could limit kwargs to search_kwargs={"k": 5}
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
    
    # Construct the LCEL chain
    chain = (
        {"context": retriever | format_docs_with_db_and_s3, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain
