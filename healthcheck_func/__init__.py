import azure.functions as func
from app.services.db_utils import DBUtils
from app.models.models import Response
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Checking cosmos db connection')
    is_healthy, message = DBUtils().db_health_check()

    response_model = Response(
        status="success" if is_healthy else "error",
        message="DB Health Check" if is_healthy else "DB Health Check Failed",
        data={"is_healthy": is_healthy},
        error=None if is_healthy else message
    )

    return func.HttpResponse(
        body= response_model.to_json(),
        status_code=200,
        mimetype="application/json"
    )