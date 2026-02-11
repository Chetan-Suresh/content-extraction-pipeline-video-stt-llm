# app/services/whisper_service.py

import whisper
import warnings

warnings.filterwarnings("ignore")

print("Loading Whisper Model...")
_model = whisper.load_model("base") 
print("Whisper Model Loaded.")

def transcribe_audio(audio_path: str) -> str:
    # This "translate" task is the magic key!
    # It tells Whisper: "Whatever language you hear, write it down in English."
    result = _model.transcribe(audio_path, task="translate")
    return result["text"]
