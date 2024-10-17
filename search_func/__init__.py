import azure.functions as func
import json
from app.models.models import SearchQuery
from app.services.semantic_search import SemanticSearch
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info('processing search query')
        # Parse request body
        req_body = req.get_json()
        query = SearchQuery(**req_body)

        # Initialize the SemanticSearch service
        semantic_search = SemanticSearch()

        # Perform the search based on the query
        results = semantic_search.search_text(query.query, query.session_id, query.limit, query.base_similarity)
        
        if not results:
            return func.HttpResponse('No results found', status_code=404)
        
        # Return success response
        return func.HttpResponse(
            json.dumps({"query": query.query, "top_results": results}),
            status_code=200,
            mimetype='application/json'
        )
    except ValueError:
        return func.HttpResponse('Invalid input', status_code=400)
    except Exception as e:
        logging.error(f"Error in search functionality: {str(e)}")
        return func.HttpResponse('Internal Server Error', status_code=500)
