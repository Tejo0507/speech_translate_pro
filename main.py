import sounddevice as sd
import numpy as np
from transformers import pipeline
import queue
import time
from app.translation import load_translator, translate
from app.tts import synthesize_speech
from app import config
