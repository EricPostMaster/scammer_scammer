# 📞 Phony Baloney — The Scam Call Delay Bot

**Phony Baloney** is an AI voice bot that answers scam calls and keeps fraudsters on the line as long as possible — wasting their time so they can't waste yours (or anyone else's).

Meet **Harold**: a confused, easily distracted elderly gentleman who *just can't find his Medicare card*. Every minute Harold holds a scammer hostage is a minute they aren't targeting a real person.

> For a full product overview, visit [`website/index.html`](website/index.html).

---

## How It Works

```
Scammer dials in
   ↓
Twilio receives the call and routes it to Harold
   ↓
Harold picks up ("Oh hello? One second dear, let me turn down the television…")
   ↓
Scammer's speech is transcribed in real time (OpenAI Whisper)
   ↓
System classifies the scam type and loads Harold's matching playbook
   ↓
Harold generates a slow, bumbling, believable response (GPT)
   ↓
Response is spoken aloud in Harold's voice (OpenAI TTS)
   ↓
Loop repeats until the scammer gives up
   ↓
Call is logged, number is flagged, metrics are updated
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Telephony** | [Twilio](https://www.twilio.com) Programmable Voice (TwiML `<Record>` + `<Play>`) |
| **Backend** | Python + FastAPI |
| **Local tunneling** | ngrok (webhook forwarding during development) |
| **Speech-to-text** | OpenAI Whisper (`gpt-4o-mini-transcribe`) |
| **LLM / Persona** | OpenAI GPT (`gpt-4o-mini`) |
| **Text-to-speech** | OpenAI TTS (`gpt-4o-mini-tts`) |
| **Storage** | JSON flat files (`call_logs.json`, `metrics.json`, `scam_knowledge.json`) |
| **Dashboard** | Streamlit |
| **Landing page** | Vanilla HTML/CSS/JS |

---

## Project Structure

```
agent.py              # Harold's conversation logic
classifier.py         # Scam-type detection
dashboard.py          # Streamlit monitoring dashboard
logger.py             # Call logging utilities
main.py               # FastAPI app + Twilio webhook handlers
report_spam.py        # Flags numbers after calls complete
stt.py                # Speech-to-text wrapper
tts.py                # Text-to-speech wrapper
data/
  call_logs.json      # Per-call transcripts and metadata
  metrics.json        # Aggregate stats
  scam_knowledge.json # Scam-type playbooks and fake data
website/
  index.html          # Landing page (full product details here)
  style.css
  main.js
```

---

## Running Locally

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the FastAPI server**
   ```bash
   uvicorn main:app --reload --port 3000
   ```

3. **Expose it via ngrok** (for Twilio webhooks)
   ```bash
   ngrok http 3000
   ```

4. **Launch the dashboard**
   ```bash
   streamlit run dashboard.py
   ```

5. Point your Twilio phone number's Voice webhook to your ngrok URL.

---

## Roadmap

- Post-call classification before auto-adding numbers to the spam registry
- OpenAI Realtime API for faster, more natural turn-taking
- Bot/robocaller detection to cut auto-dialer calls short

---

## Why This Matters

Phone scammers run call centers like businesses — the more calls they complete per hour, the more money they make. Americans lost **$81.5 billion** to scammers in 2024. If Phony Baloney can divert even a fraction of scammers' time, the increased opportunity cost could protect Americans from billions in losses by making fraud less profitable to attempt in the first place.

The best way to fight a scammer isn't to warn people. It's to make fraud *unprofitable.*
