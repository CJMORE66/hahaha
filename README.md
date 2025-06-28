# Subtitle Generator Web App

This repository contains a simple Flask-based web application that generates subtitles in a chosen language for an uploaded video file.

## Features

- Upload a video file (such as music videos or short clips).
- Automatically transcribe the audio using [Whisper](https://github.com/openai/whisper).
- Translate the transcription into the selected target language (for example, Czech).
- Download the generated subtitles as an `.srt` file.

## Requirements

- Python 3.8+
- `ffmpeg` installed and available in your system's PATH.
- Python packages listed in `requirements.txt`.

## Installation

```bash
pip install -r requirements.txt
```

## Running the App

```bash
python app.py
```

Open your browser at `http://localhost:5000` and upload a video file to generate subtitles.

## Notes

The first run may take some time as Whisper downloads its model files. For better accuracy you can change the model size in `app.py`.
