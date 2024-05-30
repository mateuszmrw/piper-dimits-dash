from typing import Union 
from bottle import HTTPResponse, Request
import json
import logging

from util.request_data import RequestData

logger = logging.getLogger(__name__)

def get_request_data(request: Request) -> Union[RequestData, HTTPResponse]:
    try:
        language = request.json.get('language')
        text = request.json.get('text')
        if not language or not text:
            raise ValueError("Missing 'language' or 'text' in the request body")
        length_scale = request.json.get('lengthScale', 1.0)
        noise_scale = request.json.get('noiseScale', 0.3)
        noise_w = request.json.get('noiseW', 1.0)

        return RequestData(language, text, length_scale, noise_scale, noise_w)

    except Exception as e:
        return handle_error(400, str(e))

def handle_error(status: int, message: str) -> HTTPResponse:
    response = {
        'status': 'error',
        'message': message
    }
    logger.error(message)
    return HTTPResponse(status=status, body=json.dumps(response))
