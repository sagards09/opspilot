import contextlib
import io

import streamlit as st

from agent import run_agent
from answer import ask_runbooks
from explain_health import explain_health
from metrics import get_health_snapshot

st.set_page_config(page_title="OpsPilot", page_icon="🛠️", layout="wide")
st.title("OpsPilot – AI Incident Assistant")
st.caption("Local LLM (Ollama) · Prometheus metrics · RAG over runbooks · AI agent")

health_tab, runbook_tab, agent_tab = st.tabs(["Health", "Ask the runbooks", "Investigate"])

# ---------- Tab 1: Health ----------
with health_tab:
    snapshot = get_health_snapshot()
    col1, col2, col3 = st.columns(3)
    col1.metric("CPU used", f"{snapshot['cpu_percent']}%")
    col2.metric("Memory used", f"{snapshot['memory_percent']}%")
    col3.metric("Disk used", f"{snapshot['disk_percent']}%")

    if st.button("Explain health with AI"):
        with st.spinner("Asking the AI..."):
            st.write(explain_health())

# ---------- Tab 2: Ask the runbooks ----------
with runbook_tab:
    question = st.text_input("Your question", "server is out of space, what should I do?")
    if st.button("Ask"):
        with st.spinner("Searching runbooks and writing the answer..."):
            st.write(ask_runbooks(question))

# ---------- Tab 3: Investigate ----------
with agent_tab:
    task = st.text_input("Alert to investigate",
                         "Disk usage alert on this server. Investigate and tell me what to do.")
    if st.button("Investigate"):
        with st.spinner("The agent is investigating..."):
            steps = io.StringIO()
            with contextlib.redirect_stdout(steps):
                answer = run_agent(task)
        st.subheader("Steps taken")
        st.code(steps.getvalue())
        st.subheader("Final answer")
        st.write(answer)