from typing import List, Dict, Any
import json
from sqlalchemy import create_engine, MetaData, Table, Column, String, Text, JSON, select, insert
from app.clients.log_storage import LogStorage
from app.core.config import settings

class PostgresLogStorage(LogStorage):
    def __init__(self):
        self.engine = create_engine(settings.POSTGRES_DSN)
        self.metadata = MetaData()
        self.query_history = Table(
            'query_history', self.metadata,
            Column('query_id', String, primary_key=True),
            Column('query', Text),
            Column('answer', Text),
            Column('logs', JSON),
        )
        self.metadata.create_all(self.engine)

    def save_logs(self, query_id: str, query: str, answer: str, logs: List[Dict[str, Any]]):
        with self.engine.connect() as conn:
            stmt = insert(self.query_history).values(
                query_id=query_id,
                query=query,
                answer=answer,
                logs=logs
            )
            conn.execute(stmt)
            conn.commit()

    def get_logs(self, query_id: str) -> Dict[str, Any]:
        with self.engine.connect() as conn:
            stmt = select(self.query_history).where(self.query_history.c.query_id == query_id)
            result = conn.execute(stmt).fetchone()
            if result:
                return {
                    "query_id": result.query_id,
                    "query": result.query,
                    "answer": result.answer,
                    "logs": result.logs
                }
            return {}
