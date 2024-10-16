import azure.functions as func
from app.services.db_utils import DBUtils
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    is_healthy, message = DBUtils().db_health_check()
    response_body = json.dumps({"is_healthy": is_healthy, "message": message})
    return func.HttpResponse(
        body=response_body,
        status_code=200,
        mimetype="application/json"
    )