# Phony Baloney — Public Website Plan

## Overview

A single-page, hero-style marketing/explainer site for **Phony Baloney**, an AI-powered scam call delay bot. The page tells the story of the problem, introduces Harold (the AI persona), explains the solution, and shows the types of scams it handles, finishing with impact stats and a dashboard teaser.

**Tone:** Warm, slightly humorous, but grounded by real-world statistics. Think "grandpa is fighting back" energy.

---

## Page Structure (Top → Bottom)

---

### Section 1 — Hero

**Purpose:** Immediately communicate the product's identity and hook the visitor.

**Layout:** Full-viewport split layout or centered with a background illustration/image.

**Visual:** A warm, illustrated or AI-generated image of **Harold** — an elderly man sitting in an armchair, phone pressed to his ear, looking pleasantly confused. A half-eaten bowl of soup and a TV remote on the side table next to him. He should look like someone's grandfather, not a tech product.

**Headline:**
> "Meet Harold. He's very confused. That's the point."

**Sub-headline:**
> Phony Baloney is an AI-powered voice bot that answers scam calls and keeps fraudsters on the line — for as long as possible.

**Primary CTA button:** `See How It Works ↓`

**Secondary CTA (optional):** `View Live Dashboard`

---

### Section 2 — The Problem

**Purpose:** Establish urgency and emotional resonance with a stark statistic.

**Layout:** Dark or high-contrast background to create a visual break. Centered text, large numbers.

**Headline:**
> The Scam Epidemic Is Costing America Billions

**Body copy:**

> In 2024, phone and online scammers cost Americans an estimated **$81.5 billion** — targeting seniors, veterans, and everyday people with fake Medicare agents, IRS threats, and romance schemes.
>
> The scammers aren't slowing down. And most of us just hang up.
>
> **What if we stopped hanging up?**

**Supporting stat callout box:**

> 💡 If Phony Baloney can divert even **0.1% of scammers' call time**, the increased opportunity cost alone could protect American citizens from nearly **$1 billion** in losses — by making scam calls less profitable to place in the first place.

**Design note:** Use large, bold typographic treatment for "$81.5 Billion" and "$1 Billion" to make the numbers impossible to ignore.

---

### Section 3 — How It Works

**Purpose:** Explain the technical pipeline in plain English without overwhelming the reader.

**Layout:** Horizontal steps (on desktop) or vertical steps (on mobile). Icons or simple numbered circles for each step.

**Section headline:**
> How Phony Baloney Works

**Steps:**

1. **Scammer Calls In**
   A known or suspected scam number dials in. Twilio receives the call and routes it to the bot.

2. **Harold Picks Up**
   The bot greets the caller in Harold's voice — an AI-generated elderly male voice — with something like: *"Oh hello? One second dear, let me turn down the television…"*

3. **We Listen & Classify**
   The scammer's speech is transcribed in real time (OpenAI Whisper). The system detects the scam type — Medicare, IRS, tech support, mortgage, romance — and loads the matching playbook.

4. **Harold Gets Confused (On Purpose)**
   A language model generates Harold's next response using a carefully crafted persona: hard of hearing, slow with information, prone to tangents about his cat or his grandson who set up the computer. Every response is designed to buy more time.

5. **Harold Talks Back**
   The response is synthesized into Harold's voice using AI text-to-speech and played back to the scammer.

6. **Repeat Until They Give Up**
   The loop continues — recording, transcribing, generating, speaking — turn after turn, wasting the scammer's most valuable resource: **time**.

**Design note:** Consider a simple animated or illustrated flowchart showing the call loop (phone → server → Harold's voice → loop back). This mirrors the architecture diagram in `project_outline.md`.

---

### Section 4 — Meet Harold

**Purpose:** Give the AI persona a human face and make the product memorable/lovable.

**Layout:** Two-column. Left: a portrait-style image of Harold (see image notes below). Right: character description.

**Image:** Harold on the phone. He should look warm and slightly bewildered — maybe squinting at a piece of paper he's pretending to read. This image should feel personal, not stock-photo-generic. Consider an illustrated portrait style rather than a photo for a more distinctive brand identity.

**Headline:**
> Meet Harold

**Body copy:**

> Harold is 77 years old. He lives alone, watches a lot of TV, and has a cat named Biscuit.
>
> He's hard of hearing. He mixes up numbers. He frequently needs to find a pen. He once spent four minutes looking for his Medicare card while narrating every step.
>
> He is also completely fictional — a persona carefully engineered to maximize the time a scammer spends on the line.
>
> Harold never breaks character. Harold never hangs up first.

**Harold's personality traits (displayed as tags or bullet points):**
- Hard of hearing
- Easily confused
- Slow with paperwork
- Goes on tangents
- Mentions his cat, Biscuit — frequently
- Grandson set up the computer
- Recently moved to a new address (can never quite remember it)

---

### Section 5 — Scam Types Harold Handles

**Purpose:** Show breadth of coverage and make the product feel robust.

**Layout:** Card grid (2×3 on desktop, scrollable on mobile). Each card represents one scam type.

**Section headline:**
> Harold Is Ready for Anything

**Cards:**

| Scam Type | Tagline | Harold's Move |
|---|---|---|
| 🏥 Medicare Fraud | "Your benefits are about to expire" | Harold slowly rhymes off a wrong Medicare ID, then corrects it, then says he needs his glasses to read it properly |
| 🏠 Mortgage Refinance | "We can lower your rate today" | Harold mentions his late wife used to handle these things, then tries to find the account number in a filing cabinet |
| ❤️ Romance Scam | "I've fallen for you..." | Harold asks them to spell their name again, then goes on a tangent about Biscuit the cat |
| 🏛️ IRS Impersonation | "You'll be arrested if you don't act now" | Harold panics just enough to seem compliant, then can't find a pencil and asks them to repeat the case number letter by letter |
| 💻 Tech Support | "Your computer has a virus" | Harold describes his screen incorrectly, asks what a browser is, and mentions he's running Windows 98 |
| 📞 Unknown / Generic | Anything else | Harold turns down the TV, asks what company they said they were from, and wonders if they have family in Utah — he has a great restaurant story |

**Design note:** The card grid gives the product a sense of intelligence and specificity without needing to explain the keyword classifier under the hood.

---

### Section 6 — The Dashboard

**Purpose:** Signal that this is a real system with real data, not a concept.

**Layout:** Full-width section with a screenshot/mockup of the Streamlit dashboard on the right, description on the left.

**Headline:**
> Every Call. Every Minute. Tracked.

**Body copy:**

> Phony Baloney logs every call in real time. The built-in dashboard shows:
>
> - **Total calls intercepted** and cumulative time wasted
> - **Call duration distribution** — so you can see just how long Harold kept them going
> - **Turns per call** — each back-and-forth exchange Harold managed to extract
> - **Scam type breakdown** — which fraud categories are most active
> - **Full turn-by-turn transcripts** — read exactly what the scammer said and how Harold responded

**Dashboard visual:** A screenshot or styled mockup of the Streamlit dashboard showing charts (call durations, turns per call, scam types bar chart) and the call log table. Ideally shown on a laptop frame graphic for polish.

---

### Section 7 — The Math

**Purpose:** Return to the impact argument with more detail, building on Section 2.

**Layout:** Centered, clean, minimal. Can use a simple calculation display.

**Headline:**
> Small Disruption. Massive Impact.

**Body copy:**

> The economics of phone scams depend on throughput. Scammers run call centers like businesses — the more calls they can complete per hour, the more money they make.
>
> Phony Baloney attacks that model directly. By tying up a scammer on a call for 3, 7, even 12 minutes, we reduce the number of real victims they can reach.

**Displayed calculation (styled prominently):**

```
$81,500,000,000  ×  0.1%  =  $81,500,000 per bot deployment (conservative)

Scale across thousands of intercepted calls → approaches $1,000,000,000 in
reduced scammer reach — without changing a single law.
```

**Closing line:**
> The best way to fight a scammer isn't to warn people. It's to make fraud unprofitable.

---

### Section 8 — Tech Stack (Footer-Adjacent "Under the Hood" Section)

**Purpose:** Credibility signal for technical visitors, investors, or journalists.

**Layout:** Simple icon + label grid or a two-column "Built With" section. Keep it brief — this is not the hero.

**Headline:**
> Built With

| Component | Technology |
|---|---|
| Telephony | Twilio Programmable Voice |
| Backend API | FastAPI (Python) |
| Speech-to-Text | OpenAI Whisper |
| Language Model | OpenAI GPT (latest mini) |
| Text-to-Speech | OpenAI TTS |
| Dashboard | Streamlit |
| Scam Knowledge Base | Curated JSON (Medicare, Mortgage, IRS, Tech Support, Romance) |

---

### Section 9 — Footer

- Project name: **Phony Baloney**
- Tagline: *"Keeping scammers busy since 2026."*
- Links (if applicable): Dashboard, GitHub, Contact
- Disclaimer: *"This project is an independent tool. It is not affiliated with any government agency or telecommunications provider."*

---

## Image Art Direction Summary

| Image | Location | Description |
|---|---|---|
| **Harold Hero Image** | Section 1 (Hero) | Harold in armchair, phone to ear, pleasantly confused expression. Warm living room setting. Bowl of soup nearby. Soft lighting. Illustrated or painterly style preferred. |
| **Harold Portrait** | Section 4 (Meet Harold) | Closer portrait crop. Harold squinting at a piece of paper, phone in hand. Slightly bemused. Same illustrated style. |
| **Dashboard Screenshot** | Section 6 | Real or mocked-up screenshot of the Streamlit dashboard showing charts and call log table. Placed inside a laptop or browser frame graphic. |
| **Call Flow Diagram** | Section 3 | Simple illustrated or diagrammatic flow: phone icon → server → Harold's voice → loop arrow back to phone. Can be built with SVG/CSS or a design tool. |

---

## Design Tokens / Style Suggestions

- **Primary color:** Warm amber or golden yellow (evokes both caution tape and a cozy grandparent's home)
- **Secondary color:** Deep navy or charcoal (for contrast sections like "The Problem")
- **Accent color:** Soft red (for scam/danger references)
- **Typography:** A friendly but serious serif for headlines (something like Playfair Display or Lora), a clean sans-serif for body (Inter or DM Sans)
- **Tone:** Not alarmist. Not silly. Smart, warm, and a little bit funny — like Harold himself.

---

## Pages / Routes (Minimal)

Since this is a single-page marketing site, all content lives on `/`. Optional additions:

- `/dashboard` → Redirects to live Streamlit dashboard
- `/about` → Brief "why we built this" if needed for press/grants

---

## Content Checklist

- [x] Hero with Harold image
- [x] $81.5B statistic (2024)
- [x] 0.1% diversion → ~$1B impact argument
- [x] How it works (technical pipeline in plain language)
- [x] Harold character introduction with second image
- [x] All 5 scam types + generic covered
- [x] Dashboard section with screenshot
- [x] Tech stack
- [x] Footer with disclaimer
