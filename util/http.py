from typing import Dict, List, Union, Any
from bottle import HTTPResponse, Request
import json
import logging

logger = logging.getLogger(__name__)


def get_request_data(request: Request, required_fields: List[str]) -> Union[Dict[str, Any], HTTPResponse]:
    data: dict[str, any] = {}
    try:
        for field in required_fields:
            value = request.json.get(field)
            if not value:
                raise ValueError(f"Missing '{field}' in the request body")
            data[field] = value
    except Exception as e:
        return handle_error(400, str(e))
    return data

def handle_error(status: int, message: str) -> HTTPResponse:
    response = {
        'status': 'error',
        'message': message
    }
    logger.error(message)
    return HTTPResponse(status=status, body=json.dumps(response))
