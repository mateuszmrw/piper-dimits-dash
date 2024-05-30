
# piper-dimits-dash

piper-dimits-dash is a web service for synthesizing audio from text using the Piper text-to-speech and Dimits library and streaming it using the DASH protocol. This service supports multiple languages and can dynamically generate audio files and DASH manifests.

## Features

- Text-to-speech synthesis for multiple languages.
- Audio streaming using DASH protocol.
- Preload models on startup.
- Configurable model options through `config.json`.

## Prerequisites

- Docker
- Python 3.x
- ffmpeg
- espeak-ng

## Installation

1. **Clone the repository:**

```sh
git clone https://github.com/yourusername/piper-dimits-dash.git
cd piper-dimits-dash
```

2. **Prepare `config.json`:**

Create a `config.json` file in the root directory if you want to customize model options:

```json
{
    "ru_RU": "ru_RU-denis-medium",
    "en_GB": "en_GB-alan-medium",
    "pl_PL": "pl_PL-darkman-medium"
}
```

3. **Build the Docker image:**

```sh
docker build -t piper-dimits-dash .
```

4. **Run the Docker container:**

```sh
docker run -p 8888:8888 -v $(pwd)/wav:/wav -v $(pwd)/models:/models piper-dimits-dash
```

To override the TEXT_MAX_LENGTH value:

```sh
docker-compose up -d --build --scale piper-dimits-dash=1 -e TEXT_MAX_LENGTH=500
```

Alternatively, you can use `docker-compose`:

```sh
docker-compose up
```

## Usage

### Endpoints

- **POST `/synthesise`**

  Synthesizes audio from text and returns the filename.

  **Request body:**

  ```json
  {
      "language": "en_GB",
      "text": "Hello, world!",
      "lengthScale": 1.0,    // Optional
      "noiseScale": 0.3,     // Optional
      "noiseW": 1.0          // Optional
  }
  ```

  **Response:**

  ```json
  {
      "status": "ok",
      "fileName": "generated_file_name"
  }
  ```

- **POST `/stream/dash`**

  Synthesizes audio and creates a DASH manifest for streaming.

  **Request body:**

  ```json
  {
      "language": "en_GB",
      "text": "Hello, world!",
      "lengthScale": 1.0,    // Optional
      "noiseScale": 0.3,     // Optional
      "noiseW": 1.0          // Optional
  }
  ```

  **Response:**

  ```json
  {
      "status": "ok",
      "manifestName": "generated_manifest_name.mpd"
  }
  ```

- **GET `/get_stream/<file_name>`**

  Retrieves the DASH manifest or audio segments.

  **Response:**

  Returns the requested file.

## Request Validation

The POST /synthesise and POST /stream/dash endpoints require a request body with specific fields. These fields are validated for type and value ranges using Pydantic models.

Request Body Fields:

- language: A string representing the language code (e.g., “en_GB”). Maximum length is 20 characters.

- text: The text to be synthesized. Maximum length is defined by the TEXT_MAX_LENGTH environment variable (default is 255 characters).

- lengthScale: An optional float value representing the length scale. Default is 1.0, with a valid range between 0.1 and 5.0.

- noiseScale: An optional float value representing the noise scale. Default is 0.3, with a valid range between 0.0 and 1.0.

-noiseW: An optional float value representing the noise weight. Default is 1.0, with a valid range between 0.0 and 1.0.

## Configuration

Model options are defined in `config.json`. If this file does not exist, default options will be used:

```json
{
    "en_GB": "en_GB-alan-medium",
}
```

## Code Overview

- **`load_model_options`**: Loads model configurations from `config.json`.
- **`preload_models`**: Preloads TTS models on startup.
- **`get_hash_name`**: Generates a SHA-1 hash for the given text.
- **`synthesise_audio_to_file`**: Synthesizes audio and saves it to a file.
- **`synthesis`**: Endpoint for synthesizing audio from text.
- **`stream_dash`**: Endpoint for creating DASH manifest and streaming audio.
- **`get_stream`**: Serves the DASH manifest and audio segments.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [Piper](https://github.com/rhasspy/piper)
- [Dimits](https://github.com/Reqeique/Dimits)
- [Bottle Web Framework](https://bottlepy.org)
- [FFmpeg](https://ffmpeg.org)

## Contributing

Feel free to submit issues, fork the repository and send pull requests. For major changes, please open an issue first to discuss what you would like to change.

---

Enjoy using piper-dimits-dash! If you have any questions or suggestions, please let us know.
