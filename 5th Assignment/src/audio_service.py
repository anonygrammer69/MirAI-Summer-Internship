import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()
GTTS_KEY = os.getenv("GTTS_KEY")


def speak(text: str, output_path: str = "output.mp3") -> str:
    """Convert story text to an MP3 file with gTTS."""
    try:
        from gtts import gTTS
    except ModuleNotFoundError as exc:
        raise RuntimeError("Install gTTS with: pip install gTTS") from exc

    if not text.strip():
        raise ValueError("Cannot generate audio for empty text.")

    audio_path = Path(output_path)
    audio_path.parent.mkdir(parents=True, exist_ok=True)

    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(str(audio_path))
    return str(audio_path)