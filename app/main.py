import sounddevice as sd
import numpy as np
from transformers import pipeline
import queue
import time
from app.tts import synthesize_speech
from app.translation import load_translator
from app import config

q = queue.Queue()

def callback(indata, frames, time_info, status):
    q.put(indata.copy())

def transcribe_english(stt, audio_np, samplerate):
    result = stt({
        "array": audio_np,
        "sampling_rate": samplerate,
        "task": "transcribe",
        "language": "en"
    })
    return result["text"]

def translate_english_to_regional(translator, english_text, tgt_lang):
    translations = translator(f">>{tgt_lang}<< {english_text}")
    return translations[0]["translation_text"]

def main():
    samplerate = config.SAMPLERATE
    buffer = []
    max_buffer_duration = config.CHUNK_SECONDS
    max_samples = max_buffer_duration * samplerate
    silence_threshold = 0.001

    print("Loading models...")
    stt = pipeline("automatic-speech-recognition", model=config.MODEL_STT, device=config.DEVICE)
    translator = load_translator()

    print("Ready to record. Speak English into the microphone...")

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
                    rms = np.sqrt(np.mean(audio_np**2))
                    if rms < silence_threshold:
                        buffer = []
                        time.sleep(0.1)
                        continue

                    english_text = transcribe_english(stt, audio_np, samplerate)
                    if english_text.strip():
                        print("📝 Transcribed (English):", english_text)
                        tgt_lang = 'te'  
                        translated_text = translate_english_to_regional(translator, english_text, tgt_lang)
                        print("🌍 Translated (Regional):", translated_text)
                        synthesize_speech(translated_text, lang=tgt_lang)
                    else:
                        print("No speech detected.")
                    buffer = []

                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nStopped recording.")

if _name_ == "_main_":
    main()