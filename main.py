import os
import traceback
import time
from fastapi import FastAPI, Form
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv
from pathlib import Path

import agent
import logger

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")

app = FastAPI(title="Scam Call Delay Bot")

# Serve generated TTS audio files
Path("audio").mkdir(exist_ok=True)
app.mount("/audio", StaticFiles(directory="audio"), name="audio")


def twiml_response(content: str) -> Response:
    return Response(content=content, media_type="application/xml")


@app.post("/incoming")
def incoming_call(CallSid: str = Form(...)):
    """Twilio hits this endpoint when a call arrives."""
    try:
        print(f"[INCOMING] CallSid: {CallSid}")
        logger.init_call(CallSid)

        # Generate greeting with the bot's voice instead of Twilio's default
        greeting_text = "Oh hello? One second dear, let me turn down the television..."
        greeting_audio = agent.get_greeting(greeting_text, CallSid)

        resp = VoiceResponse()
        if greeting_audio:
            resp.play(f"{BASE_URL}/audio/{greeting_audio}")
        else:
            # Fallback to Twilio voice if TTS fails
            resp.say(greeting_text, voice="Polly.Joanna")
        
        resp.record(
            action=f"{BASE_URL}/process_audio",
            method="POST",
            max_length=10,
            play_beep=False,
            timeout=3,
        )
        print(f"[INCOMING] Response created successfully")
        return twiml_response(str(resp))
    except Exception as e:
        print(f"[ERROR] /incoming failed: {e}")
        traceback.print_exc()
        # Return a valid TwiML response even on error
        resp = VoiceResponse()
        resp.say("Sorry, there was a technical error. Please try again later.")
        return twiml_response(str(resp))


@app.post("/process_audio")
def process_audio(
    CallSid: str = Form(...),
    RecordingUrl: str = Form(...),
    CallStatus: str = Form(default="in-progress"),
):
    """Twilio hits this endpoint after each recording segment."""
    request_start = time.time()
    try:
        print(f"[PROCESS_AUDIO] CallSid: {CallSid[:8]}..., Status: {CallStatus}")
        
        if CallStatus in ("completed", "canceled", "failed"):
            # Call ended — return empty TwiML
            print(f"[PROCESS_AUDIO] Call ended with status: {CallStatus}")
            return twiml_response(str(VoiceResponse()))

        audio_url = RecordingUrl + ".mp3"
        print(f"[PROCESS_AUDIO] Starting agent.handle_turn()...")
        
        handle_turn_start = time.time()
        audio_file = agent.handle_turn(audio_url, CallSid)
        handle_turn_duration = time.time() - handle_turn_start
        
        print(f"[PROCESS_AUDIO] agent.handle_turn() completed in {handle_turn_duration*1000:.0f}ms")

        resp = VoiceResponse()

        if audio_file:
            resp.play(f"{BASE_URL}/audio/{audio_file}")
        else:
            # Fallback if TTS failed
            resp.say("Hold on dear, I'm still looking for that paper.", voice="Polly.Joanna")

        # Loop — record the next segment
        resp.record(
            action=f"{BASE_URL}/process_audio",
            method="POST",
            max_length=10,
            play_beep=False,
            timeout=3,
        )
        
        total_request_time = time.time() - request_start
        print(f"[PROCESS_AUDIO] Complete request handled in {total_request_time*1000:.0f}ms")
        return twiml_response(str(resp))
    except Exception as e:
        print(f"[ERROR] /process_audio failed: {e}")
        traceback.print_exc()
        # Return a valid TwiML response even on error
        resp = VoiceResponse()
        resp.say("Sorry, there was a technical error. Please try again later.")
        return twiml_response(str(resp))


@app.get("/health")
def health():
    return {"status": "ok"}
