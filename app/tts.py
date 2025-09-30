from gtts import gTTS
import sounddevice as sd
import soundfile as sf
import os
import tempfile

def synthesize_speech(text, lang='en'):
    if not text.strip():
        return
    tts = gTTS(text=text, lang=lang)
    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        tts.save(path)
        data, fs = sf.read(path, dtype='float32')
        sd.play(data, fs)
        sd.wait()
    finally:
        os.remove(path)
