from fastapi import APIRouter, HTTPException
from app.models.models import SearchQuery, TextInput
from app.services.semantic_search import SemanticSearch

router = APIRouter()

@router.post("/text")
async def add_text(text_input: TextInput):
    if not SemanticSearch().store_text(text_input.text, text_input.session_id):
        raise HTTPException(status_code=500, detail="Error storing text")
    return {"message": "Text stored successfully"}

@router.post("/search")
async def search(query: SearchQuery):
    results = SemanticSearch().search_text(query.query, query.session_id, query.limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No results found")
    return {"query": query.query, "top_results": results}