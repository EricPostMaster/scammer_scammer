import uuid
import os
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

Path("audio").mkdir(exist_ok=True)

# ElevenLabs voice IDs for elderly-sounding female voices
# Find more at https://elevenlabs.io/app/voice-library
ELEVENLABS_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # "Bella" - warm, older-sounding female


def synthesize(text: str, call_id: str) -> str:
    """Convert text to speech using ElevenLabs (primary) or OpenAI (fallback)."""
    filename = f"{call_id}_{uuid.uuid4().hex[:6]}.mp3"
    path = Path("audio") / filename

    # Try ElevenLabs first (faster)
    if elevenlabs_api_key:
        try:
            from elevenlabs.client import ElevenLabs
            client = ElevenLabs(api_key=elevenlabs_api_key)
            # Use streaming to start writing chunks immediately
            audio_stream = client.text_to_speech.convert_as_stream(
                text=text,
                voice_id=ELEVENLABS_VOICE_ID,
                model_id="eleven_flash_v2",
                output_format="mp3_44100_128"
            )
            with open(path, "wb") as f:
                for chunk in audio_stream:
                    f.write(chunk)
            print(f"[TTS] Used ElevenLabs for synthesis (streaming)")
            return filename
        except Exception as e:
            print(f"[TTS] ElevenLabs failed: {e}, falling back to OpenAI")

    # Fallback to OpenAI
    try:
        response = openai_client.audio.speech.create(
            model="tts-1",
            voice="nova",   # warm, older-sounding female voice
            input=text,
        )
        response.stream_to_file(path)
        print(f"[TTS] Used OpenAI for synthesis")
        return filename
    except Exception as e:
        print(f"[TTS] OpenAI also failed: {e}")
        raise


