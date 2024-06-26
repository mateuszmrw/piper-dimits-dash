FROM python:slim

WORKDIR /app
RUN apt-get update && apt-get install espeak-ng ffmpeg libsm6 libxext6 -y

COPY . .
RUN pip install -r requirements.txt        
ENV TEXT_MAX_LENGTH=255

CMD [ "python", "main.py" ]
