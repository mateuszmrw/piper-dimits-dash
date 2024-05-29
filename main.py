from dimits import Dimits
from bottle import route, request, static_file, run
import hashlib
from ffmpeg import FFmpeg

import json
import os

audio_dir = "/wav"
models_dir = "/models"

def load_model_options() -> dict[str, str]:
    model_file_exists = os.path.isfile("config.json")
    if model_file_exists == False:
        return {
            "ru_RU": "ru_RU-denis-medium",
            "en_GB": "en_GB-alan-medium",
            "pl_PL": "pl_PL-darkman-medium",
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
       wav_exists = os.path.isfile(audio_dir + "/" + file_name + ".wav")

       if wav_exists == False:
        dt = Dimits(model)
        dt.text_2_audio_file(text, file_name, audio_dir, format="wav")

       return file_name

@route('/synthesise', method='POST')
def synthesis():
       language = request.json.get('language')
       text = request.json.get("text")
       model = model_options.get(language)
       if model == None:
              return json.dumps({ 'status': "No model for the language" })
       fileName = synthesise_audio_to_file(text, model)

       return json.dumps({'status': "ok", 'fileName': fileName })

@route('/stream/dash', method='POST')
def stream_dash():
       language = request.json.get('language')
       text = request.json.get("text")
       model = model_options.get(language)
       if model == None:
              return json.dumps({ 'status': "No model for the language" })

       manifest_name = get_hash_name(text) + ".mpd"
       manifest_exist = os.path.isfile(audio_dir + "/" + manifest_name)
       if manifest_exist == True:
        return json.dumps({'status': "ok", 'manifestName': manifest_name })

       file_name = synthesise_audio_to_file(text, model)
       wav_file_name = file_name + ".wav"

       if manifest_exist == False:
        ffmpeg = (
                FFmpeg()
                .option("y")
                .input(audio_dir + "/" + wav_file_name)
                .output(audio_dir + "/" + manifest_name, f="dash")
        )

        ffmpeg.execute()
        os.remove(audio_dir + "/" + wav_file_name)
       return json.dumps({'status': "ok", 'manifestName': manifest_name })

@route('/get_stream/<file_name>', method='GET')
def get_stream(file_name):
       return static_file(file_name, root=audio_dir)

run(host='0.0.0.0', port=8888, reloader=True, debug=True)

