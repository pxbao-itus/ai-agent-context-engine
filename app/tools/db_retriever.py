from sqlalchemy import create_engine, MetaData, Table, Column, String, Text, select
from app.core.config import settings

# Using standard sqlalchemy to simulate fetching chunks from Postgres
engine = create_engine(settings.POSTGRES_DSN)
metadata = MetaData()

# Define a simple table schema for the chunks
document_chunks = Table(
    'document_chunks', metadata,
    Column('chunk_id', String, primary_key=True),
    Column('document_id', String),
    Column('content', Text),
)

def fetch_chunk_content(chunk_ids: list[str]) -> list[dict]:
    """Fetches full content natively from Postgres for a bunch of chunk IDs returned by Qdrant metadata."""
    if not chunk_ids:
        return []
        
    try:
        with engine.connect() as conn:
            stmt = select(document_chunks).where(document_chunks.c.chunk_id.in_(chunk_ids))
            result = conn.execute(stmt)
            return [{"chunk_id": row.chunk_id, "document_id": row.document_id, "content": row.content} for row in result]
    except Exception as e:
        print(f"Failed to fetch from DB: {e}")
        return []
