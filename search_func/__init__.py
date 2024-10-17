import azure.functions as func
import json
from app.models.models import SearchQuery
from app.services.semantic_search import SemanticSearch
from app.models.models import Response
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
            response_model = Response(
                status="error",
                message="No results found",
                error="No results found"
            )
            return func.HttpResponse(response_model.to_json(), status_code=404, mimetype='application/json')

        
        # Return success response
        response_model = Response(
            status="success",
            message="Search results returned successfully",
            data={"query": query.query, "top_results": results}
        )
        return func.HttpResponse(response_model.to_json(), status_code=200, mimetype='application/json')

    except ValueError:
        response_model = Response(
            status="error",
            message="Invalid input",
            error="Invalid input"
        )
        return func.HttpResponse(response_model.to_json(), status_code=400, mimetype='application/json')

    
    except Exception as e:
        logging.error(f"Error in search functionality: {str(e)}")
        response_model = Response(
            status="error",
            message="Search failed",
            error=str(e)
        )
        return func.HttpResponse(response_model.to_json(), status_code=500, mimetype='application/json')