from dimits import Dimits
from dimits.ttsmodel import TextToSpeechModel as ttsm

from bottle import route, request, static_file, run, HTTPResponse
import hashlib
from ffmpeg import FFmpeg

import json
import os

import logging

from util.http import get_request_data, handle_error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

audio_dir = "/wav"
models_dir = "/models"
audio_format = "wav"

def load_model_options() -> dict[str, str]:
    model_file_exists = os.path.isfile("config.json")
    if model_file_exists == False:
        return {
            "en_GB": "en_GB-alan-medium",
        }
    with open("config.json") as f:
         config = json.load(f)
         return config

model_options = load_model_options()
def preload_models(model_options: dict[str, str]):
     for value in model_options.values():
          Dimits(value, True, models_dir)

preload_models(model_options)

def get_hash_name(text: str) -> str:
    return hashlib.sha1(text.encode("UTF-8")).hexdigest()

def synthesise_audio_to_file(text: str, model: str) -> str:
       file_name = get_hash_name(text)
       wav_exists = os.path.isfile(f'{audio_dir}/${file_name}.{audio_format}')

       if wav_exists == False:
        dt = Dimits(model, True, models_dir)
        dt.text_2_audio_file(text, file_name, audio_dir, format="wav")

       return file_name

@route('/synthesise', method='POST')
def synthesis() -> HTTPResponse:
    try:
        required_fields = ["language", "text"]
        data = get_request_data(request, required_fields)
        if isinstance(data, HTTPResponse):
            return data
        model = model_options.get(data["language"])
        if model is None:
            return handle_error(404, "No model available for the specified language")

        fileName = synthesise_audio_to_file(data["text"], model)
        return json.dumps({'status': "ok", 'fileName': fileName })
    
    except Exception as e:
        return handle_error(500, f"Internal server error: {str(e)}")

@route('/stream/dash', method='POST')
def stream_dash() -> HTTPResponse:
    try:
        required_fields = ["language", "text"]
        data = get_request_data(request, required_fields)
        if isinstance(data, HTTPResponse):
            return data

        model = model_options.get(data["language"])
        if model is None:
            return handle_error(404, "No model available for the specified language")

        manifest_name = f'{get_hash_name(data["text"])}.mpd'
        manifest_exist = os.path.isfile(f'{audio_dir}/{manifest_name}')
        if manifest_exist:
            return json.dumps({'status': "ok", 'manifestName': manifest_name })

        file_name = synthesise_audio_to_file(data["text"], model)

        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(f'{audio_dir}/{file_name}.{audio_format}')
            .output(f'{audio_dir}/{manifest_name}', f="dash")
        )

        ffmpeg.execute()
        os.remove(f'{audio_dir}/{file_name}.{audio_format}')
        return json.dumps({'status': "ok", 'manifestName': manifest_name })
    
    except Exception as e:
        return handle_error(500, f"Internal server error: {str(e)}")

@route('/get_stream/<file_name>', method='GET')
def get_stream(file_name):
       return static_file(file_name, root=audio_dir)

run(host='0.0.0.0', port=8888, reloader=True, debug=True)

