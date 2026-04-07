import json
from pathlib import Path

with open(Path(__file__).parent / "data" / "scam_knowledge.json") as f:
    KNOWLEDGE = json.load(f)

# Cache the detected scam type per call so we only classify once
_call_types: dict[str, str] = {}


def detect(transcript: str, call_id: str) -> str:
    """Return the scam type for this call, cached after first detection."""
    if call_id in _call_types:
        return _call_types[call_id]

    text = transcript.lower()
    for scam_type, data in KNOWLEDGE.items():
        if scam_type == "generic":
            continue
        if any(kw in text for kw in data.get("keywords", [])):
            _call_types[call_id] = scam_type
            return scam_type

    # Don't cache generic — maybe the next turn has more context
    return "generic"
