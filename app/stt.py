from transformers import pipeline
import app.config as config

def load_stt():
    return pipeline("automatic-speech-recognition", model=config.MODEL_STT, device=config.DEVICE)

def transcribe(stt_model, np_audio):
    result = stt_model({
        "array": np_audio,
        "sampling_rate": config.SAMPLERATE,
        "task": "transcribe",
        "language": config.LANGUAGE
    })
    return result["text"]
