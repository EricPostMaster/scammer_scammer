Yeah — this is a super common frustration with ElevenLabs. The short answer is:

👉 **Tags like `[laugh]`, `[sigh]`, etc. are *not reliably interpreted*** by their TTS models — so they often get spoken literally.

To make voices sound *actually real*, you need to shift from “stage directions” → **writing for speech + using the right API features**.

---

# 🔑 What actually works (and why)

## 1. Write like a human speaks (not like a script)

Instead of:

```
Hi there. [laugh] That’s funny.
```

Write:

```
Hi there… haha, that’s actually pretty funny.
```

👉 The model understands **phonetic cues**, not abstract tags.

### Examples that work better:

* `[laugh]` → `"haha"` / `"heh"` / `"that’s funny"`
* `[sigh]` → `"... yeah."` / `"alright..."` / `"okay."`
* `[pause]` → use `...` or commas
* `[excited]` → punctuation + wording:

  * `"No way!! That’s amazing!"`

---

## 2. Use punctuation as prosody control

ElevenLabs models heavily rely on punctuation:

* `...` → longer pause, reflective tone
* `,` → short pause
* `—` → interruption / shift
* `!` → energy
* `?` → rising tone

👉 This is one of the **most powerful levers** you have.

---

## 3. Tune voice settings (this matters a LOT)

When calling the API, use `voice_settings`:

```json
{
  "stability": 0.35,
  "similarity_boost": 0.75,
  "style": 0.6,
  "use_speaker_boost": true
}
```

### What these do:

* **stability (↓ = more expressive)**

  * 0.2–0.4 → natural, emotional
  * 0.7+ → robotic, consistent
* **style (↑ = more dramatic delivery)**
* **similarity_boost**

  * Keeps voice consistent (don’t max it out)

👉 For realism:
**Lower stability + moderate style = more human**

---

## 4. Stream instead of generating full blocks

Use streaming (`/stream` endpoint) so the model behaves more like live speech.

👉 This reduces:

* over-polished cadence
* unnatural pacing

---

## 5. Break text into conversational chunks

Don’t send long paragraphs.

Instead:

```js
[
  "Hey — is this Bob?",
  "Cool. I’m Alice.",
  "Quick question for you..."
]
```

👉 Then generate audio per chunk.

This:

* improves pacing
* allows natural pauses
* avoids “monologue voice”

---

## 6. Inject disfluencies (VERY important)

Real humans are imperfect.

Add things like:

* “uh”
* “um”
* “you know”
* “I mean”
* slight repetition

Example:

```
So, uh… I was thinking — maybe we could try that again?
```

👉 This alone can 10x realism.

---

## 7. Don’t rely on LLM stage directions

If you're using something like OpenAI or another LLM to generate dialogue:

### ❌ Bad prompt:

> Include [laughs], [pauses], etc.

### ✅ Better prompt:

> Write natural spoken dialogue including hesitations, filler words, and conversational tone.

---

## 8. Advanced: phonetic nudging

You can subtly control tone with wording:

* “right.” → sounds firm
* “right?” → sounds unsure
* “okay…” → reflective
* “okay!” → upbeat

---

# 🔧 Example (Node + ElevenLabs API)

```js
import fetch from "node-fetch";

const text = "Hey… haha, yeah — that’s actually pretty funny.";

const response = await fetch(
  "https://api.elevenlabs.io/v1/text-to-speech/YOUR_VOICE_ID",
  {
    method: "POST",
    headers: {
      "xi-api-key": process.env.ELEVENLABS_API_KEY,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      text,
      model_id: "eleven_multilingual_v2",
      voice_settings: {
        stability: 0.35,
        similarity_boost: 0.75,
        style: 0.6
      }
    })
  }
);
```

---

# 🧠 Key mindset shift

👉 You’re not “telling the model what to do”
👉 You’re **giving it text that already *sounds* like speech**

---

# If you want next level realism

I can help you implement:

* real-time turn-taking (interruptions, barge-in)
* memory-aware conversational flow
* dynamic tone switching based on user sentiment
* voice personas (customer support vs friend vs interviewer)

Just tell me 👍
