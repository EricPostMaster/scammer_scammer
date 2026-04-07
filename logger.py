import json
import time
from pathlib import Path

LOGS_FILE = Path("data/call_logs.json")
METRICS_FILE = Path("data/metrics.json")


def _load(path: Path) -> dict:
    if path.exists() and path.stat().st_size > 0:
        return json.loads(path.read_text())
    return {}


def _save(path: Path, data: dict):
    path.write_text(json.dumps(data, indent=2))


def init_call(call_id: str):
    """Record the start of a new call."""
    logs = _load(LOGS_FILE)
    logs[call_id] = {
        "start_time": time.time(),
        "scam_type": "unknown",
        "turns": [],
        "conversation": []
    }
    _save(LOGS_FILE, logs)


def log_turn(call_id: str, transcript: str, response: str, scam_type: str, timings: dict = None):
    """Append a turn to the call log with timing details and refresh aggregated metrics."""
    if timings is None:
        timings = {}
    
    logs = _load(LOGS_FILE)
    entry = logs.setdefault(call_id, {
        "start_time": time.time(), 
        "turns": [],
        "conversation": [],
        "scam_type": "unknown"
    })
    
    # Ensure conversation key exists (defensive)
    if "conversation" not in entry:
        entry["conversation"] = []
    
    turn_number = len(entry["turns"]) + 1
    turn_entry = {
        "turn": turn_number,
        "timestamp": time.time(),
        "caller_transcript": transcript,
        "bot_response": response,
        "scam_type": scam_type,
    }
    
    # Add timing details if provided
    if timings:
        turn_entry["timings_ms"] = {k: round(v * 1000, 1) for k, v in timings.items()}
    
    entry["turns"].append(turn_entry)
    
    # Add to conversation log with clear labels
    entry["conversation"].append({"role": "caller", "text": transcript, "timestamp": time.time()})
    entry["conversation"].append({"role": "bot", "text": response, "timestamp": time.time()})
    
    entry["scam_type"] = scam_type
    entry["end_time"] = time.time()
    _save(LOGS_FILE, logs)
    _update_metrics(call_id, entry)
    
    # Print timing info to console for real-time visibility
    if timings:
        total_ms = timings.get('total', 0) * 1000
        print(f"[TURN_COMPLETE] Call={call_id[:8]}... | Total={total_ms:.0f}ms | "
              f"STT={timings.get('stt', 0)*1000:.0f}ms | "
              f"LLM={timings.get('llm', 0)*1000:.0f}ms | "
              f"TTS={timings.get('tts', 0)*1000:.0f}ms | "
              f"Classify={timings.get('classify', 0)*1000:.0f}ms")


def _update_metrics(call_id: str, entry: dict):
    metrics = _load(METRICS_FILE)
    if "calls" not in metrics:
        metrics["calls"] = []

    record = {
        "call_id": call_id,
        "duration": round(entry.get("end_time", 0) - entry.get("start_time", 0), 1),
        "turns": len(entry["turns"]),
        "scam_type": entry.get("scam_type", "unknown"),
    }

    # Upsert by call_id
    for i, c in enumerate(metrics["calls"]):
        if c["call_id"] == call_id:
            metrics["calls"][i] = record
            break
    else:
        metrics["calls"].append(record)

    _save(METRICS_FILE, metrics)
