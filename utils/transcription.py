# import whisper
#
# model = whisper.load_model("base")
#
# def transcribe_audio(file_path):
#     result = model.transcribe(file_path, word_timestamps=True)
#     return result['text'], result['segments']


import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path, word_timestamps=True)
    return result["text"], result["segments"]
