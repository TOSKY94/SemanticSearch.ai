import azure.functions as func
import json
from app.models.models import SearchQuery, TextInput
from app.services.semantic_search import SemanticSearch
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        route = req.route_params.get('route')
        logging.info(f"Route received: {route}")
        
        if route == 'text':
            return handle_add_text(req)
        elif route == 'search':
            return handle_search(req)
        elif route == 'healthcheck':
            return func.HttpResponse('Semantic Search API is running!', status_code=200)
        else:
            return func.HttpResponse('Route not found', status_code=404)
        
    except Exception as e:
        logging.error(f"Error in route handling: {str(e)}")
        return func.HttpResponse('Internal Server Error', status_code=500)
    
def handle_add_text(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        text_input = TextInput(**req_body)
        semantic_search = SemanticSearch()
        success, chunks = semantic_search.store_text(text_input.text, text_input.session_id, text_input.chunk_size)
        
        if not success:
            return func.HttpResponse('Error storing text', status_code=500)
        
        return func.HttpResponse(json.dumps({"message": "Text stored successfully", "chunks": chunks}), status_code=200)
    except ValueError:
        return func.HttpResponse('Invalid input', status_code=400)

def handle_search(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        query = SearchQuery(**req_body)
        semantic_search = SemanticSearch()
        results = semantic_search.search_text(query.query, query.session_id, query.limit, query.base_similarity)
        
        if not results:
            return func.HttpResponse('No results found', status_code=404)
        
        return func.HttpResponse(json.dumps({"query": query.query, "top_results": results}), status_code=200)
    except ValueError:
        return func.HttpResponse('Invalid input', status_code=400)