from transformers import pipeline
from app import config

def load_stt():
    return pipeline("automatic-speech-recognition", model=config.MODEL_STT, device=config.DEVICE)

def transcribe(stt_model, np_audio):
    return stt_model({"array": np_audio, "sampling_rate": config.SAMPLERATE, "language": config.LANGUAGE})
