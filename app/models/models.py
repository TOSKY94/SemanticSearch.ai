from pydantic import BaseModel

class TextInput(BaseModel):
    session_id: str
    text: str
    chunk_size: int = 100

class SearchQuery(BaseModel):
    session_id: str
    query: str
    limit: int = 10