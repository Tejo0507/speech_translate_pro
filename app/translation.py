from transformers import pipeline
import app.config as config

def load_translator(tgt_lang):
    model_name = config.MODEL_TRANSLATION.get(tgt_lang)
    if not model_name:
        raise ValueError(f"Unsupported target language: {tgt_lang}")
    return pipeline("translation", model=model_name, device=config.DEVICE)

def translate(translator, text):
    return translator(text)[0]["translation_text"]
