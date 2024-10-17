import azure.functions as func
from app.services.db_utils import DBUtils
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Checking cosmos db connection')
    is_healthy, message = DBUtils().db_health_check()
    response_body = json.dumps({"is_healthy": is_healthy, "message": message})
    return func.HttpResponse(
        body=response_body,
        status_code=200,
        mimetype="application/json"
    )