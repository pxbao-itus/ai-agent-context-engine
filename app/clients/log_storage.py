from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LogStorage(ABC):
    @abstractmethod
    def save_logs(self, query_id: str, query: str, answer: str, logs: List[Dict[str, Any]]):
        """Saves the query, result, and all associated logs."""
        pass

    @abstractmethod
    def get_logs(self, query_id: str) -> Dict[str, Any]:
        """Retrieves logs for a specific query."""
        pass
