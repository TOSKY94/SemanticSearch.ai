from fastapi import APIRouter, HTTPException
from app.models.models import SearchQuery, TextInput
from app.services.semantic_search import SemanticSearch

router = APIRouter()

@router.post("/text")
async def add_text(text_input: TextInput):
    semantic_search = SemanticSearch()
    result = semantic_search.store_text(text_input.text, text_input.session_id, text_input.chunk_size)
    if not result[0]:
        raise HTTPException(status_code=500, detail="Error storing text")
    return {"message": "Text stored successfully", "chunks": result[1]}

@router.post("/search")
async def search(query: SearchQuery):
    semantic_search = SemanticSearch()
    results = semantic_search.search_text(query.query, query.session_id, query.limit, query.base_similarity)
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    
    return {"query": query.query, "top_results": results}