import azure.functions as func
import json
from app.models.models import TextInput
from app.services.semantic_search import SemanticSearch
from app.models.models import Response
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info('processing and storing text embeddings')
        # Parse request body
        req_body = req.get_json()
        text_input = TextInput(**req_body)

        # Initialize the SemanticSearch service
        semantic_search = SemanticSearch()

        # Store the text, chunk it, and vectorize
        success, chunks = semantic_search.store_text(text_input.text, text_input.session_id, text_input.chunk_size)
        
        if not success:
            response_model = Response(
                status="error",
                message="Error storing text"
            )
            return func.HttpResponse(response_model.to_json(), status_code=500, mimetype='application/json')
        
        # Return success response
        response_model = Response(
            status="success",
            message="Text stored successfully",
            data={"chunks_stored": chunks}
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
        logging.error(f"Error in text storage: {str(e)}")
        response_model = Response(
            status="error",
            message="Text storage failed",
            error=str(e)
        )

        return func.HttpResponse(response_model.to_json(), status_code=500, mimetype='application/json')
