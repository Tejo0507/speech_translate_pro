from transformers import pipeline
from app import config

def load_translator():
    return pipeline("translation", model=config.MODEL_TRANSLATION, device=config.DEVICE)

def translate(translator, text, tgt_lang):
    return translator(text, tgt_lang=tgt_lang)[0]["translation_text"]
