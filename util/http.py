from bottle import HTTPResponse 
import json
import logging

logger = logging.getLogger(__name__)

def handle_error(status: int, message: str) -> HTTPResponse:
    response = {
        'status': 'error',
        'message': message
    }
    logger.error(message)
    return HTTPResponse(status=status, body=json.dumps(response))
