import pyttsx3

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
    
    def synthesize(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

tts_engine = TextToSpeech()

def synthesize_speech(text):
    tts_engine.synthesize(text)
