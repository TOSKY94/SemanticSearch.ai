import azure.functions as func
import json
from app.models.models import TextInput
from app.services.semantic_search import SemanticSearch
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
            return func.HttpResponse(json.dumps({'error': 'Error storing text'}),
                                     status_code=500, mimetype='application/json')
        
        # Return success response
        return func.HttpResponse(
            json.dumps({"message": "Text stored successfully", "chunks": chunks}),
            status_code=200,
            mimetype='application/json'
        )
    except ValueError:
        return func.HttpResponse(json.dumps({'error': 'Invalid input'}),
                                     status_code=400, mimetype='application/json')
    except Exception as e:
        logging.error(f"Error in text storage: {str(e)}")
        return func.HttpResponse(json.dumps({'error': str(e)}), status_code=500, mimetype='application/json')
