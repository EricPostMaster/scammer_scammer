import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(page_title="Scam Bot Dashboard", layout="wide")
st.title("Scam Call Delay Bot — Dashboard")

metrics_path = Path("data/metrics.json")
logs_path = Path("data/call_logs.json")


def load_metrics() -> pd.DataFrame:
    if not metrics_path.exists():
        return pd.DataFrame()
    data = json.loads(metrics_path.read_text())
    calls = data.get("calls", [])
    if not calls:
        return pd.DataFrame()
    return pd.DataFrame(calls)


def load_logs() -> dict:
    if not logs_path.exists():
        return {}
    return json.loads(logs_path.read_text())


# Auto-refresh
if st.button("Refresh"):
    st.rerun()

df = load_metrics()

if df.empty:
    st.info("No call data yet. Waiting for calls...")
    st.stop()

# ── Top metrics ────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Calls", len(df))
col2.metric("Avg Duration (s)", round(df["duration"].mean(), 1))
col3.metric("Avg Turns", round(df["turns"].mean(), 1))
col4.metric("Total Time Wasted (s)", int(df["duration"].sum()))

st.divider()

# ── Charts ─────────────────────────────────────────────────────────────────────
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Call Duration (seconds)")
    st.bar_chart(df.set_index("call_id")["duration"])

with chart_col2:
    st.subheader("Turns per Call")
    st.bar_chart(df.set_index("call_id")["turns"])

st.subheader("Scam Types Encountered")
scam_counts = df["scam_type"].value_counts().reset_index()
scam_counts.columns = ["scam_type", "count"]
st.bar_chart(scam_counts.set_index("scam_type")["count"])

st.divider()

# ── Call log table ─────────────────────────────────────────────────────────────
st.subheader("Call Log")
st.dataframe(df, use_container_width=True)

# ── Turn-by-turn transcript viewer ────────────────────────────────────────────
st.subheader("Turn Transcripts")
logs = load_logs()
if logs:
    selected_call = st.selectbox("Select a call", list(logs.keys()))
    entry = logs[selected_call]
    st.caption(
        f"Scam type: **{entry.get('scam_type', 'unknown')}** | "
        f"Turns: **{len(entry.get('turns', []))}**"
    )
    for i, turn in enumerate(entry.get("turns", []), 1):
        with st.expander(f"Turn {i}"):
            st.markdown(f"**Scammer:** {turn.get('transcript', '')}")
            st.markdown(f"**Bot:** {turn.get('response', '')}")
