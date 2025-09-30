import shutil
import os
from pathlib import Path

cache_dir = Path.home() / ".cache" / "tts_models" / "tts_models" / "en" / "ljspeech" / "tacotron2-DDC"
if cache_dir.exists():
    shutil.rmtree(cache_dir)
    print("Deleted corrupted model folder:", cache_dir)
else:
    print("Model folder not found, no deletion needed.")
