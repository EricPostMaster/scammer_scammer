The project is a "scam call delay bot" that receives calls from scam numbers and then draws the conversation out as long as possible to keep the scammer busy so they can't be calling a real person.

---

# 1) System Architecture (End-to-End)

**Core flow (turn-based voice loop):**

```
Scammer (phone)
   ↓
Twilio Voice Webhook
   ↓
[Backend API (FastAPI)]
   ↓
1. Record caller speech (Twilio <Record>)
2. Send audio → STT (OpenAI Whisper)
3. Classify scam type (LLM or rule-based)
4. Retrieve tactics + fake data (JSON “vector store”)
5. Generate response (LLM w/ persona + tactics)
6. Convert text → speech (OpenAI TTS)
7. Return TwiML <Play> audio
   ↓
Repeat loop
```

---

# 2) Tech Stack (Opinionated + Minimal)

### Telephony

* [Twilio](https://www.twilio.com?utm_source=chatgpt.com)

  * Use **Programmable Voice**
  * TwiML `<Record>` + `<Play>`

### Backend

* Python + **FastAPI**
* Ngrok (for local webhook testing)

### AI Layer

* [OpenAI Platform](https://platform.openai.com?utm_source=chatgpt.com)

  * **Speech-to-text**: `gpt-4o-mini-transcribe` (fast + cheap)
  * **LLM reasoning**: `gpt-5-mini` (low latency)
  * **Text-to-speech**: `gpt-4o-mini-tts`

### Storage (Hackathon-grade)

* JSON files:

  * `scam_knowledge.json`
  * `call_logs.json`
  * `metrics.json`

### Frontend Dashboard

* **Streamlit**

---

# 3) Data Design (Critical for Agent Quality)

## 3.1 “Vector Store” (JSON)

Structure it like this:

```json
{
  "medicare": {
    "keywords": ["medicare", "benefits", "coverage"],
    "tactics": [
      "ask them to repeat frequently",
      "misread ID numbers",
      "pretend to look for documents slowly"
    ],
    "fake_data": {
      "medicare_id": ["AB12345", "AB12346", "wait sorry AB12365"],
      "ssn": ["123-45-6789", "123-45-6798"],
      "address": ["742 Evergreen Terrace", "no wait 724... I always mix that up"]
    }
  },
  "mortgage": {...},
  "romance": {...}
}
```

## 3.2 Retrieval Strategy (Simple but Effective)

Per turn:

1. Detect scam type (once, early)
2. Load corresponding tactics + fake data
3. Inject into prompt dynamically

No embeddings needed—keyword matching is enough.

---

# 4) Agent Loop (Core Logic)

## 4.1 Pseudocode

```python
def handle_turn(audio_file, call_id):

    transcript = transcribe(audio_file)

    scam_type = detect_scam_type(transcript, call_id)

    context = load_context(scam_type)

    response = generate_response(
        transcript,
        context,
        persona="elderly, hard of hearing, easily confused",
        objective="maximize call duration"
    )

    audio_response = text_to_speech(response)

    log_turn(call_id, transcript, response, scam_type)

    return audio_response
```

---

## 4.2 Prompt Design (This is your “secret sauce”)

### System Prompt

```
You are an elderly person on the phone.

Traits:
- Hard of hearing (frequently ask them to repeat)
- Easily confused
- Slow with information
- Often misstate numbers and correct yourself
- Occasionally go off on small tangents

Primary goal:
Maximize the length of the call.

Tactics:
- Ask clarifying questions repeatedly
- Pretend to search for documents
- Provide incorrect information, then correct it
- Stall naturally (not obviously)

Never break character.
Never end the conversation abruptly.
```

### Dynamic Injection

```
Scam type: Medicare

Available fake data:
- Medicare ID: AB12345, AB12346...
- SSN: 123-45-6789...

Relevant tactics:
- Misread numbers
- Ask for repetition
```

---

# 5) Twilio Implementation (Concrete)

## 5.1 Incoming Call Webhook

Return TwiML:

```xml
<Response>
  <Say>Oh hello? One second dear...</Say>
  <Record action="/process_audio" maxLength="10" />
</Response>
```

## 5.2 After Recording

* Twilio hits `/process_audio`
* You:

  * Download recording
  * Run agent loop
  * Return:

```xml
<Response>
  <Play>https://your-server.com/audio/response.mp3</Play>
  <Record action="/process_audio" maxLength="10" />
</Response>
```

This creates a **looping conversation**.

---

# 6) Metrics + Logging (“Wow Factor”)

## 6.1 What to Track

Per call:

* `call_id`
* `start_time`
* `end_time`
* `duration_seconds`
* `num_turns`
* `scam_type`

Per turn:

* transcript
* response

## 6.2 JSON Example

```json
{
  "calls": [
    {
      "call_id": "123",
      "duration": 180,
      "turns": 12,
      "scam_type": "medicare"
    }
  ]
}
```

---

# 7) Streamlit Dashboard

### Charts to Implement

* Histogram: call durations
* Histogram: turns per call
* Bar chart: scam types

### Minimal Code Concept

```python
import streamlit as st
import pandas as pd

df = pd.read_json("metrics.json")

st.title("Scam Call Delay Bot Dashboard")

st.subheader("Call Duration Distribution")
st.bar_chart(df["duration"])

st.subheader("Turns per Call")
st.bar_chart(df["turns"])

st.subheader("Scam Types")
st.bar_chart(df["scam_type"].value_counts())
```

---

# 8) Build Plan (2.5 Days)

## Day 1 (Core Pipeline)

* Twilio webhook setup
* FastAPI server
* Audio recording loop working
* STT + TTS wired up
* Hardcoded responses

## Day 2 (Agent Intelligence)

* Prompt engineering
* Scam classification
* JSON “vector store”
* Dynamic response generation
* Logging + metrics

## Day 2.5 (Polish + Demo)

* Streamlit dashboard
* Improve persona realism
* Add “funny delays” (key demo win)
* Test 2–3 scripted scam scenarios

---

# 9) Demo Strategy (Important)

Script your demo calls:

1. “Medicare scam”
2. “Mortgage refinance”
3. “Romance scam”

Show:

* Live call snippet
* Dashboard updating
* Highlight:

  * “This call lasted 4 minutes”
  * “Bot gave 3 wrong SSNs before correcting”

---

# 10) High-Impact Enhancements (If Time Allows)

* Add **intent detection per turn** (what scammer is asking for)
* Introduce **delays** (sleep 1–2s before responding)
* Randomized personality quirks
* “Interruptions” like:

  * “Hold on, my TV is loud…”