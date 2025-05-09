# app.py
from flask import Flask, request, jsonify
from utils.transcription import transcribe_audio
from utils.accuracy import calculate_accuracy
from utils.speed import calculate_wpm
from utils.fluency import detect_fluency
from utils.pronunciation import get_pronunciation_feedback
import os
from werkzeug.utils import secure_filename
from pydub import AudioSegment

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/evaluate', methods=['POST'])
def evaluate():
    audio_file = request.files['audio']
    expected_text = request.form['expected_text']

    filename = secure_filename(audio_file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    audio_file.save(file_path)

    transcript, segments = transcribe_audio(file_path)
    accuracy = calculate_accuracy(transcript, expected_text)
    total_duration = segments[-1]['end'] - segments[0]['start']
    wpm = calculate_wpm(len(transcript.split()), total_duration)
    fluency = detect_fluency(segments)
    pron_feedback = get_pronunciation_feedback(transcript, expected_text)

    # Overall score (example logic)
    score = f"{round((accuracy/100 + wpm/100 + (1 if fluency == 'excellent' else 0.8 if fluency == 'good' else 0.5))/3 * 5, 1)} / 5 stars"

    return jsonify({
        "accuracy": f"{accuracy}%",
        "speed": f"{wpm} WPM",
        "fluency": fluency,
        "pron_feedback": pron_feedback,
        "score": score
    })

if __name__ == '__main__':
    app.run(debug=True)
