import httpx
from openai import OpenAI
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def transcribe(audio_url: str) -> str:
    """Download a Twilio recording and transcribe it with Whisper."""
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    # Twilio recordings require HTTP Basic Auth
    response = httpx.get(audio_url, auth=(account_sid, auth_token), follow_redirects=True)
    response.raise_for_status()

    tmp = Path("tmp_audio.mp3")
    tmp.write_bytes(response.content)

    with tmp.open("rb") as f:
        result = client.audio.transcriptions.create(model="whisper-1", file=f)

    return result.text
