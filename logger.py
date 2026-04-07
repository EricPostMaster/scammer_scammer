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
    logs[call_id] = {"start_time": time.time(), "scam_type": "unknown", "turns": []}
    _save(LOGS_FILE, logs)


def log_turn(call_id: str, transcript: str, response: str, scam_type: str):
    """Append a turn to the call log and refresh aggregated metrics."""
    logs = _load(LOGS_FILE)
    entry = logs.setdefault(call_id, {"start_time": time.time(), "turns": []})
    entry["turns"].append({"transcript": transcript, "response": response})
    entry["scam_type"] = scam_type
    entry["end_time"] = time.time()
    _save(LOGS_FILE, logs)
    _update_metrics(call_id, entry)


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
