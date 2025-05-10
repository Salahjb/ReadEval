from flask import Flask, request, jsonify, render_template
from utils.transcription import transcribe_audio
from utils.accuracy import calculate_accuracy
from utils.speed import calculate_wpm
from utils.fluency import detect_fluency
from utils.pronunciation import get_pronunciation_feedback
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    dummy_text = (
        "The quick brown fox jumps over the lazy dog. "
        "It was a bright sunny day, and the birds were singing in the trees. "
        "Suddenly, the fox stopped and listened carefully. "
        "Something was moving in the bushes nearby."
    )
    return render_template('index.html', dummy_text=dummy_text)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    audio_file = request.files['audio']
    expected_text = request.form['expected_text']

    if not audio_file or audio_file.filename == '':
        return jsonify({"error": "No audio file uploaded"}), 400

    # Save original audio
    original_filename = secure_filename(audio_file.filename)
    base_filename = f"{uuid.uuid4().hex}_{original_filename.rsplit('.', 1)[0]}"
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    audio_file.save(original_path)

    # Convert to WAV
    converted_path = os.path.join(app.config['UPLOAD_FOLDER'], base_filename + ".wav")
    audio = AudioSegment.from_file(original_path)
    audio.export(converted_path, format="wav")

    # Transcription & alignment
    transcript, segments = transcribe_audio(converted_path)

    # Metrics
    accuracy = calculate_accuracy(transcript, expected_text)
    total_duration = segments[-1]['end'] - segments[0]['start']
    wpm = calculate_wpm(len(transcript.split()), total_duration)
    fluency = detect_fluency(segments)
    pron_feedback = get_pronunciation_feedback(transcript, expected_text)

    # Score (example logic)
    score = round(
        (accuracy / 100 + wpm / 100 + (1 if fluency == 'excellent' else 0.8 if fluency == 'good' else 0.5)) / 3 * 5, 1
    )

    result = {
        "accuracy": f"{accuracy}%",
        "speed": f"{wpm} WPM",
        "fluency": fluency,
        "pron_feedback": pron_feedback,
        "score": f"{score} / 5 stars"
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
