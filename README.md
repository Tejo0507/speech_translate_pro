# Speech Translator Pro

## Objective
This project is a real-time speech translation application that captures English speech input, transcribes it, translates it to selected regional languages (Hindi, Tamil, Telugu), and outputs the translated speech. It aims to facilitate communication across language barriers using speech-to-text, translation, and text-to-speech technologies.

## Tech Stack
- **Python 3.11**: Core programming language.
- **Streamlit**: Web app framework providing UI and interaction.
- **Transformers (Hugging Face)**: For automatic speech recognition (Whisper) and machine translation models.
- **SoundDevice**: For audio recording from microphone.
- **gTTS (Google Text-to-Speech)**: For speech synthesis of translated text.
- **NumPy**: For audio data manipulation.
- **PyTorch**: Backend for deep learning model execution.
- **Other Libraries**:
  - Queue: for buffer management of streaming audio data.

## Implementation Details
- Streamlit app records streaming microphone audio, buffers audio chunks.
- Uses Hugging Face Whisper model for real-time English speech-to-text transcription.
- Selected regional language via UI dropdown triggers translation using Helsinki-NLP models.
- Translated text is synthesized back to speech using gTTS.
- Supports dark/light mode UI toggling and audio playback within the app.
- Manages audio streaming latency with chunk buffering and silence detection for efficient processing.

## Program Explanation and Flow

- `streamlit_app.py` loads the UI framework, CSS style, and launches the app by calling `main()` from `app/main.py`.
- `app/main.py` drives the user interface, manages audio recording streams, buffers audio, sends audio chunks to the Whisper model for transcription, sends transcribed text to translation models, renders outputs, and controls synthesis playback.
- `app/tts.py` handles generating speech audio from translated text using Google's Text-To-Speech API.
- `app/translation.py` loads translation models from pretrained Hugging Face checkpoints and performs English-to-target language translation using those models.
- `app/config.py` contains centralized configuration values used throughout the project for easy maintenance and tuning.

The flow from spoken English → transcribed text → translated text → synthesized speech happens continuously and is managed chiefly by `main.py`.

## How to Run

1. **Clone the repository:**

2. **Install dependencies:**
It's recommended to use a virtual environment.
pip install -r requirements.txt


3. **Run the Streamlit app:**
streamlit run streamlit_app.py


4. **Use the app UI:**
- Select the target language from the dropdown.
- Click "Record and Translate".
- Speak in English clearly into your microphone.
- The app will transcribe, translate, and play back the translated speech.
- Use the dark/light mode toggle button in the top right corner to switch themes.

Make sure you have your microphone connected and working for audio input.

## Screenshots

<img width="1840" height="931" alt="image" src="https://github.com/user-attachments/assets/6c8f5e4c-89a0-4415-9f77-cb226b689b05" />
<img width="1790" height="918" alt="image" src="https://github.com/user-attachments/assets/c0051e3b-b5db-4ef7-86b8-b6db336c6fef" />

