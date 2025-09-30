import streamlit as st
import numpy as np
import sounddevice as sd
import tempfile
import os
from transformers import pipeline
from gtts import gTTS
from app import config
from app.translation import load_translator


def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


@st.cache_resource
def load_models():
    stt_model = pipeline("automatic-speech-recognition", model=config.MODEL_STT, device=config.DEVICE)
    translator = load_translator()
    return stt_model, translator


def synthesize_and_play(text, lang='en'):
    if not text or not text.strip():
        st.warning("No text available for speech synthesis.")
        return
    tts = gTTS(text=text, lang=lang)
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    tts.save(path)
    audio_bytes = open(path, "rb").read()
    os.remove(path)
    st.audio(audio_bytes, format="audio/mp3")


def record_audio(duration, samplerate):
    st.info(f"Recording for {duration} seconds... Speak clearly.")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    st.success("Recording complete")
    return np.squeeze(recording)


def main():
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

    load_css()

    col1, col2 = st.columns([9, 1])
    with col1:
        st.markdown(
            "<div class='wrapper'><h1>🎤 English to Regional Language Speech Translation</h1>",
            unsafe_allow_html=True,
        )
    with col2:
        if st.button("🌓", key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode

    language_map = {"Telugu": "te", "Tamil": "ta", "Hindi": "hi"}

    st.markdown('<div class="selectbox-wrapper">', unsafe_allow_html=True)
    target_lang_name = st.selectbox("", options=list(language_map.keys()), key="select", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    duration = st.slider("", 1, 10, 5, key="slider", label_visibility="collapsed")

    if st.button("Record and Translate", key="btn"):
        np_audio = record_audio(duration, config.SAMPLERATE)
        stt_model, translator = load_models()
        with st.spinner("Transcribing..."):
            result = stt_model({
                "array": np_audio,
                "sampling_rate": config.SAMPLERATE,
                "task": "transcribe",
                "language": "en"
            })
        english_text = result["text"]
        st.markdown(f"<div class='result-box'>📝 <b>Transcribed (English):</b><br>{english_text}</div>", unsafe_allow_html=True)
        with st.spinner("Translating..."):
            tgt_lang = language_map[target_lang_name]
            translated_text = translator(f">>{tgt_lang}<< {english_text}")[0]["translation_text"]
        st.markdown(f"<div class='result-box'>🌍 <b>Translated ({target_lang_name}):</b><br>{translated_text}</div>", unsafe_allow_html=True)
        synthesize_and_play(translated_text, lang=tgt_lang)

    about_html = """
        <div class="about-btn">
            <a href="#" target="_blank">About</a>
        </div>
    </div>
    """
    st.markdown(about_html, unsafe_allow_html=True)

    if st.session_state.dark_mode:
        st.markdown("""
        <style>
            .stApp { background-color: #121212 !important; color: #fff !important; }
            .wrapper { border-color: rgba(255, 255, 255, 0.447) !important; color: #fff !important; background: transparent !important; }
            .btn { background-color: #fff !important; color: #333 !important; }
            .about-btn a { color: #4caf50 !important; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .stApp { background-color: #fff !important; color: #000 !important; }
            .wrapper { border-color: rgba(0,0,0,0.1) !important; color: #000 !important; background: rgba(255, 255, 255, 0.85) !important; }
            .btn { background-color: #1976d2 !important; color: white !important; }
            .about-btn a { color: #1976d2 !important; }
        </style>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()