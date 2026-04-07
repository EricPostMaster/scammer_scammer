# Scam Call Delay Bot — Implementation Plan

## Project Structure

```
scammer_scammer/
├── main.py                  # FastAPI app + Twilio webhooks
├── agent.py                 # Core agent loop
├── tts.py                   # Text-to-speech helper
├── stt.py                   # Speech-to-text helper
├── classifier.py            # Scam type detection
├── logger.py                # Call/turn logging
├── dashboard.py             # Streamlit dashboard
├── data/
│   ├── scam_knowledge.json  # Tactics + fake data per scam type
│   ├── call_logs.json       # Per-turn transcripts/responses
│   └── metrics.json         # Aggregated call metrics
├── audio/                   # Temp TTS output files
├── .env                     # API keys
└── requirements.txt
```

---

## Dependencies

```
fastapi
uvicorn
twilio
openai
python-dotenv
streamlit
pandas
httpx
```

---

## Phase 1 — Twilio Webhook + Recording Loop

### `main.py`

```python
from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Record, Play, Say
import agent, logger

app = FastAPI()

@app.post("/incoming")
def incoming_call(CallSid: str = Form(...)):
    resp = VoiceResponse()
    resp.say("Oh hello? One second dear...")
    resp.record(action="/process_audio", max_length=10, play_beep=False)
    logger.init_call(CallSid)
    return Response(content=str(resp), media_type="application/xml")

@app.post("/process_audio")
def process_audio(CallSid: str = Form(...), RecordingUrl: str = Form(...)):
    audio_url = RecordingUrl + ".mp3"
    audio_path = agent.handle_turn(audio_url, CallSid)

    resp = VoiceResponse()
    resp.play(f"https://<your-ngrok>/audio/{audio_path}")
    resp.record(action="/process_audio", max_length=10, play_beep=False)
    return Response(content=str(resp), media_type="application/xml")
```

Serve the `audio/` directory as static files:

```python
from fastapi.staticfiles import StaticFiles
app.mount("/audio", StaticFiles(directory="audio"), name="audio")
```

---

## Phase 2 — Agent Loop

### `agent.py`

```python
import stt, tts, classifier, logger
from openai import OpenAI
import json, time

client = OpenAI()

with open("data/scam_knowledge.json") as f:
    KNOWLEDGE = json.load(f)

SYSTEM_PROMPT = """
You are an elderly person on the phone.
- Hard of hearing, ask them to repeat often
- Easily confused, slow with information
- Misstate numbers, then correct yourself
- Occasionally go off on brief tangents
Goal: maximize call length. Never end the call. Never break character.
"""

def handle_turn(audio_url: str, call_id: str) -> str:
    transcript = stt.transcribe(audio_url)
    scam_type = classifier.detect(transcript, call_id)
    context = KNOWLEDGE.get(scam_type, KNOWLEDGE["generic"])

    dynamic = f"""
Scam type: {scam_type}
Tactics: {', '.join(context['tactics'])}
Fake data: {json.dumps(context['fake_data'])}
"""
    time.sleep(1.5)  # natural delay before responding

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT + dynamic},
            {"role": "user", "content": transcript},
        ]
    ).choices[0].message.content

    audio_file = tts.synthesize(response, call_id)
    logger.log_turn(call_id, transcript, response, scam_type)
    return audio_file
```

---

## Phase 3 — STT + TTS

### `stt.py`

```python
import httpx
from openai import OpenAI

client = OpenAI()

def transcribe(audio_url: str) -> str:
    audio_bytes = httpx.get(audio_url).content
    with open("tmp_audio.mp3", "wb") as f:
        f.write(audio_bytes)
    with open("tmp_audio.mp3", "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1", file=f
        )
    return result.text
```

### `tts.py`

```python
import uuid
from openai import OpenAI
from pathlib import Path

client = OpenAI()

def synthesize(text: str, call_id: str) -> str:
    filename = f"{call_id}_{uuid.uuid4().hex[:6]}.mp3"
    path = Path("audio") / filename
    response = client.audio.speech.create(
        model="tts-1", voice="nova", input=text
    )
    response.stream_to_file(path)
    return filename
```

---

## Phase 4 — Scam Classification

### `classifier.py`

```python
import json

with open("data/scam_knowledge.json") as f:
    KNOWLEDGE = json.load(f)

# Cache detected type per call to avoid re-classifying every turn
_call_types: dict[str, str] = {}

def detect(transcript: str, call_id: str) -> str:
    if call_id in _call_types:
        return _call_types[call_id]

    text = transcript.lower()
    for scam_type, data in KNOWLEDGE.items():
        if any(kw in text for kw in data.get("keywords", [])):
            _call_types[call_id] = scam_type
            return scam_type

    _call_types[call_id] = "generic"
    return "generic"
```

---

## Phase 5 — Knowledge Store

### `data/scam_knowledge.json`

```json
{
  "medicare": {
    "keywords": ["medicare", "benefits", "coverage", "card"],
    "tactics": [
      "ask them to repeat the ID number twice",
      "misread numbers and correct yourself",
      "pretend to search for your card slowly"
    ],
    "fake_data": {
      "medicare_id": ["AB12345", "wait sorry... AB12365"],
      "ssn": ["123-45-6789", "no wait 123-45-6798"],
      "address": ["742 Evergreen Terrace", "no wait 724... I always mix that up"]
    }
  },
  "mortgage": {
    "keywords": ["mortgage", "refinance", "loan", "interest rate"],
    "tactics": [
      "ask them to explain the rate again",
      "pretend to look for your account number",
      "mention your late husband used to handle these things"
    ],
    "fake_data": {
      "account": ["00123456", "wait let me find the paper"],
      "balance": ["$187,000", "or maybe $178,000"]
    }
  },
  "romance": {
    "keywords": ["love", "relationship", "money", "western union", "gift card"],
    "tactics": [
      "ask how they are doing at length",
      "go on tangents about your cat",
      "pretend to be writing things down slowly"
    ],
    "fake_data": {
      "name": ["Dorothy", "Dot"],
      "card_number": ["4111 1111 1111...", "hold on I need my glasses"]
    }
  },
  "generic": {
    "keywords": [],
    "tactics": [
      "ask them to repeat themselves",
      "pretend to look for a pen"
    ],
    "fake_data": {
      "name": ["Harold"],
      "phone": ["555-010-1234"]
    }
  }
}
```

---

## Phase 6 — Logging

### `logger.py`

```python
import json, time
from pathlib import Path

LOGS_FILE = Path("data/call_logs.json")
METRICS_FILE = Path("data/metrics.json")

def _load(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}

def init_call(call_id: str):
    logs = _load(LOGS_FILE)
    logs[call_id] = {"start_time": time.time(), "turns": []}
    LOGS_FILE.write_text(json.dumps(logs, indent=2))

def log_turn(call_id: str, transcript: str, response: str, scam_type: str):
    logs = _load(LOGS_FILE)
    entry = logs.setdefault(call_id, {"start_time": time.time(), "turns": []})
    entry["turns"].append({"transcript": transcript, "response": response})
    entry["scam_type"] = scam_type
    entry["end_time"] = time.time()
    LOGS_FILE.write_text(json.dumps(logs, indent=2))
    _update_metrics(call_id, entry)

def _update_metrics(call_id: str, entry: dict):
    metrics = _load(METRICS_FILE)
    metrics.setdefault("calls", [])
    existing = next((c for c in metrics["calls"] if c["call_id"] == call_id), None)
    record = {
        "call_id": call_id,
        "duration": entry.get("end_time", 0) - entry.get("start_time", 0),
        "turns": len(entry["turns"]),
        "scam_type": entry.get("scam_type", "unknown"),
    }
    if existing:
        metrics["calls"][metrics["calls"].index(existing)] = record
    else:
        metrics["calls"].append(record)
    METRICS_FILE.write_text(json.dumps(metrics, indent=2))
```

---

## Phase 7 — Streamlit Dashboard

### `dashboard.py`

```python
import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(page_title="Scam Bot Dashboard", layout="wide")
st.title("Scam Call Delay Bot")

metrics_path = Path("data/metrics.json")
if not metrics_path.exists():
    st.warning("No call data yet.")
    st.stop()

data = json.loads(metrics_path.read_text())
df = pd.DataFrame(data["calls"])

col1, col2, col3 = st.columns(3)
col1.metric("Total Calls", len(df))
col2.metric("Avg Duration (s)", round(df["duration"].mean(), 1))
col3.metric("Avg Turns", round(df["turns"].mean(), 1))

st.subheader("Call Duration Distribution")
st.bar_chart(df.set_index("call_id")["duration"])

st.subheader("Turns per Call")
st.bar_chart(df.set_index("call_id")["turns"])

st.subheader("Scam Types")
st.bar_chart(df["scam_type"].value_counts())

st.subheader("Call Log")
st.dataframe(df, use_container_width=True)
```

Run with: `streamlit run dashboard.py`

---

## Environment Setup

### `.env`

```
OPENAI_API_KEY=sk-...
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
```

### Local Testing with Ngrok

```bash
# Terminal 1
uvicorn main:app --reload --port 8000

# Terminal 2
ngrok http 8000
```

Set Twilio webhook URL to: `https://<ngrok-id>.ngrok.io/incoming`

---

## Build Order

| Step | Task | File(s) |
|------|------|---------|
| 1 | Twilio webhook + recording loop | `main.py` |
| 2 | STT + TTS wired to real audio | `stt.py`, `tts.py` |
| 3 | Hardcoded agent response (smoke test) | `agent.py` |
| 4 | Scam classifier + knowledge store | `classifier.py`, `scam_knowledge.json` |
| 5 | Full LLM-driven agent with persona | `agent.py` |
| 6 | Logging per turn + metrics | `logger.py` |
| 7 | Streamlit dashboard | `dashboard.py` |
| 8 | Polish: delays, tangents, better fake data | `agent.py`, `scam_knowledge.json` |

---

## Key Risk / Mitigations

| Risk | Mitigation |
|------|-----------|
| Twilio recording auth (403) | Append Twilio credentials to download URL or use `twilio` SDK to fetch recording |
| Audio file not served in time | Write TTS file before returning TwiML; ensure static mount is correct |
| High latency per turn | Use `tts-1` (not HD), `whisper-1`, and `gpt-4o-mini`; add `stream=True` if needed |
| LLM breaks character | Reinforce "Never break character" in system prompt; add a fallback canned response |
