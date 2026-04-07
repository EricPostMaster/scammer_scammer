import uuid
import os
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

Path("audio").mkdir(exist_ok=True)


def synthesize(text: str, call_id: str) -> str:
    """Convert text to speech, save to audio/, return the filename."""
    filename = f"{call_id}_{uuid.uuid4().hex[:6]}.mp3"
    path = Path("audio") / filename

    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",   # warm, older-sounding female voice
        input=text,
    )
    response.stream_to_file(path)
    return filename
