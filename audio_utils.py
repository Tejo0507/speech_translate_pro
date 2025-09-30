import sounddevice as sd
import numpy as np
import queue

def create_audio_queue():
    return queue.Queue()

def make_callback(q):
    def callback(indata, frames, time, status):
        q.put(indata.copy())
    return callback

def get_audio_stream(samplerate, channels, callback):
    return sd.InputStream(samplerate=samplerate, channels=channels, callback=callback)
