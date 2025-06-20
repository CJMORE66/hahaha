from flask import Flask, request, render_template, send_file
import tempfile
import whisper
from googletrans import Translator
import os

app = Flask(__name__)


def format_timestamp(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'video' not in request.files:
            return 'No video uploaded', 400
        file = request.files['video']
        if file.filename == '':
            return 'No selected file', 400
        language = request.form.get('language', 'cs')
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            file.save(tmp.name)
            model = whisper.load_model('base')
            result = model.transcribe(tmp.name)
        translator = Translator()
        srt_entries = []
        for i, segment in enumerate(result['segments'], 1):
            translated = translator.translate(segment['text'], dest=language).text
            start = format_timestamp(segment['start'])
            end = format_timestamp(segment['end'])
            srt_entries.append(f"{i}\n{start} --> {end}\n{translated}\n")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.srt', mode='w', encoding='utf-8') as srt_file:
            srt_file.write('\n'.join(srt_entries))
        return send_file(srt_file.name, as_attachment=True, download_name='subtitles.srt')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
