import os
from typing import Union
from pydantic import BaseModel, Field, ValidationError
from bottle import HTTPResponse, Request

from util.http import handle_error 

TEXT_MAX_LENGTH = int(os.getenv('TEXT_MAX_LENGTH', 255))

class RequestData(BaseModel):
    language: str = Field(..., max_length=20)
    text: str = Field(..., max_length=TEXT_MAX_LENGTH)
    length_scale: float = Field(default=1.0, ge=0.1, le=1.0)
    noise_scale: float = Field(default=0.3, ge=0.0, le=1.0)
    noise_w: float = Field(default=1.0, ge=0.0, le=1.0)

    @classmethod
    def from_json(cls, data: dict):
        transformed_data = {
            'language': data.get('language'),
            'text': data.get('text'),
            'length_scale': data.get('lengthScale', 1.0),
            'noise_scale': data.get('noiseScale', 0.3),
            'noise_w': data.get('noiseW', 1.0)
        }
        try:
            return cls(**transformed_data)
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e}")

def get_request_data(request: Request) -> Union[RequestData, HTTPResponse]:
    try:
        data = request.json
        return RequestData.from_json(data)
    except ValidationError as e:
        return handle_error(400, str(e))