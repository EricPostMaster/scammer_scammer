import streamlit as st
import pandas as pd
import json
from pathlib import Path
import altair as alt

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
    duration_bins = list(range(0, int(df["duration"].max() + 20), 20))
    duration_binned = pd.cut(df["duration"], bins=duration_bins)
    duration_hist = duration_binned.value_counts().sort_index()
    duration_hist = duration_hist.reset_index()
    duration_hist.columns = ["Duration Range (seconds)", "Count"]
    duration_hist["Duration Range (seconds)"] = duration_hist["Duration Range (seconds)"].astype(str)
    chart1 = alt.Chart(duration_hist).mark_bar().encode(
        x=alt.X("Duration Range (seconds):N", axis=alt.Axis(labelAngle=0), scale=alt.Scale(paddingInner=0)),
        y="Count:Q"
    ).properties(width=500, height=400)
    st.altair_chart(chart1, use_container_width=True)

with chart_col2:
    st.subheader("Turns per Call")
    turns_bins = list(range(0, int(df["turns"].max()) + 2))
    turns_binned = pd.cut(df["turns"], bins=turns_bins)
    turns_hist = turns_binned.value_counts().sort_index()
    turns_hist = turns_hist.reset_index()
    turns_hist.columns = ["Turn Count", "Count"]
    turns_hist["Turn Count"] = turns_hist["Turn Count"].astype(str)
    chart2 = alt.Chart(turns_hist).mark_bar().encode(
        x=alt.X("Turn Count:N", axis=alt.Axis(labelAngle=0), scale=alt.Scale(paddingInner=0)),
        y="Count:Q"
    ).properties(width=500, height=400)
    st.altair_chart(chart2, use_container_width=True)

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
