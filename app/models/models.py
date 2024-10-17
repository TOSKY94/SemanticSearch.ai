from pydantic import BaseModel
import json
from typing import Any, Optional

class TextInput(BaseModel):
    session_id: str
    text: str
    chunk_size: int = 100

class SearchQuery(BaseModel):
    session_id: str
    query: str
    limit: int = 10
    base_similarity: float = 0.5

class Response:
    def __init__(self, status: str, message: str, data: Optional[Any] = None, error: Optional[str] = None):
        self.status = status
        self.message = message
        self.data = data
        self.error = error

    def to_json(self):
        response = {
            "status": self.status,
            "message": self.message,
        }

        if self.data is not None:
            response["data"] = self.data
        if self.error is not None:
            response["error"] = self.error

        return json.dumps(response)