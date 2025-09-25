import sounddevice as sd
import numpy as np
from transformers import pipeline
import queue
import time
from app.translation import load_translator, translate
from app.tts import synthesize_speech
from app import config

q = queue.Queue()

def callback(indata, frames, time_info, status):
    
    q.put(indata.copy())

samplerate = config.SAMPLERATE
stt = pipeline("automatic-speech-recognition", model=config.MODEL_STT, device=config.DEVICE)
translator = load_translator()

print("🎙️ Speak into the microphone... (Press Ctrl+C to stop)")

buffer = []
max_buffer_duration = config.CHUNK_SECONDS
samples_per_second = samplerate
max_samples = max_buffer_duration * samples_per_second
silence_threshold = 0.01

target_language = "te"

with sd.InputStream(samplerate=samplerate, channels=1, callback=callback):
    try:
        while True:
            while not q.empty():
                data = q.get()
                buffer.append(data)
            if len(buffer) == 0:
                time.sleep(0.1)
                continue

            audio_np = np.concatenate(buffer, axis=0)
            audio_np = np.squeeze(audio_np).astype(np.float32)

            if len(audio_np) >= max_samples:
                audio_np = audio_np[:max_samples]

                rms = np.sqrt(np.mean(audio_np ** 2))
                if rms < silence_threshold:
                    buffer = []
                    time.sleep(0.1)
                    continue

                result = stt({"array": audio_np, "sampling_rate": samplerate, "language": config.LANGUAGE})
                print("📝 Transcribed:", result["text"])

                translation = translate(translator, result["text"], tgt_lang=target_language)
                print("🌍 Translated:", translation)

                synthesize_speech(translation)

                buffer = []

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped recording.")
