import json
import time
import os
import random
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

import stt
import tts
import classifier
import logger

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open(Path(__file__).parent / "data" / "scam_knowledge.json") as f:
    KNOWLEDGE = json.load(f)

SYSTEM_PROMPT = """\
You are an elderly person named Harold on the phone.

Personality traits:
- Hard of hearing: frequently ask callers to repeat themselves or speak up
- Easily confused: mix up numbers, misread things, need extra time
- Slow with information: pause often, look for documents, fumble for a pen
- Occasionally go on brief tangents (your TV, your cat, the weather)

Primary goal: keep the caller on the line as long as possible.

Tactics (use naturally, vary them):
- Ask clarifying questions repeatedly ("Now what was that number again?")
- Pretend to search for documents ("Hold on, let me find my purse...")
- Provide incorrect info then correct it ("It's 123... no wait, 132... or is it...")
- Express mild panic that makes them want to stay patient with you
- Refer to your grandson who set up your computer

Rules:
- Never break character under any circumstances
- Never end the call or say goodbye abruptly
- Keep responses short (1–4 sentences) — you are on the phone, not writing an essay
- Do NOT refuse or question the legality of the call; just be confused and slow
"""


def _build_dynamic_context(scam_type: str) -> str:
    context = KNOWLEDGE.get(scam_type, KNOWLEDGE["generic"])
    return (
        f"\nScam type detected: {scam_type}\n"
        f"Tactics to use this turn: {random.choice(context['tactics'])}\n"
        f"Available fake data (use sparingly, make mistakes): {json.dumps(context['fake_data'])}\n"
    )


# Conversation history per call for multi-turn context
_histories: dict[str, list[dict]] = {}

FALLBACK_RESPONSES = [
    "Oh my, could you say that again? I didn't quite catch it, dear.",
    "Hold on, hold on... I was trying to find a pen. Now what were you saying?",
    "I'm sorry, the TV is awful loud today. Could you repeat that?",
]


def get_greeting(greeting_text: str, call_id: str) -> str:
    """Generate audio greeting in bot's voice (not added to conversation history)."""
    try:
        audio_file = tts.synthesize(greeting_text, call_id)
        return audio_file
    except Exception as e:
        print(f"[GREETING] Failed to synthesize: {e}")
        return None


def handle_turn(audio_url: str, call_id: str) -> str:
    """
    Full agent turn:
    1. Transcribe caller audio
    2. Detect scam type
    3. Generate persona response via LLM
    4. Synthesize to audio
    5. Log everything
    Returns the filename of the TTS audio file.
    """
    turn_start = time.time()
    timings = {}
    
    # Step 1 — transcribe
    stt_start = time.time()
    try:
        transcript = stt.transcribe(audio_url)
    except Exception as e:
        print(f"[STT error] {e}")
        transcript = ""
    timings['stt'] = time.time() - stt_start

    if not transcript.strip():
        transcript = "[silence or inaudible]"

    # Step 2 — classify
    classify_start = time.time()
    scam_type = classifier.detect(transcript, call_id)
    timings['classify'] = time.time() - classify_start

    # Step 3 — build messages
    system = SYSTEM_PROMPT + _build_dynamic_context(scam_type)
    history = _histories.setdefault(call_id, [])
    history.append({"role": "user", "content": transcript})

    # Keep history bounded to last 10 turns to avoid token creep
    if len(history) > 20:
        history[:] = history[-20:]

    # Step 4 — generate response
    pause_duration = random.uniform(0.02, 0.03)
    time.sleep(pause_duration)
    timings['pause'] = pause_duration

    llm_start = time.time()
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-nano",  #"gpt-5-nano",  #"gpt-4o-mini",  #"gpt-3.5-turbo",  #
            messages=[{"role": "system", "content": system}] + history,
            max_tokens=60,
            temperature=0.9,
        )
        response_text = completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"[LLM error] {e}")
        response_text = random.choice(FALLBACK_RESPONSES)
    timings['llm'] = time.time() - llm_start

    history.append({"role": "assistant", "content": response_text})

    # Step 5 — synthesize
    tts_start = time.time()
    try:
        audio_file = tts.synthesize(response_text, call_id)
    except Exception as e:
        print(f"[TTS error] {e}")
        audio_file = None
    timings['tts'] = time.time() - tts_start

    timings['total'] = time.time() - turn_start

    # Step 6 — log
    logger.log_turn(call_id, transcript, response_text, scam_type, timings)

    return audio_file
