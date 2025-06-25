"""Streamlit dashboard for managing automation workflows."""

from __future__ import annotations

import sys
from io import StringIO
from pathlib import Path
from contextlib import redirect_stdout

import yaml
import streamlit as st

# Ensure project root is on the Python path so we can import modules
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from run_workflow import run_workflow


st.title("AutomationAgent Dashboard")

workflow_dir = ROOT_DIR / "workflows"
workflow_files = sorted(p.name for p in workflow_dir.glob("*.yaml"))

st.sidebar.header("Workflow")
selected = st.sidebar.selectbox("Select workflow", workflow_files)

# Load selected workflow content into session state
if (
    "workflow_text" not in st.session_state
    or st.session_state.get("selected_workflow") != selected
):
    st.session_state.selected_workflow = selected
    st.session_state.workflow_text = (workflow_dir / selected).read_text()

st.subheader("Workflow YAML")
st.session_state.workflow_text = st.text_area(
    "Edit steps below", st.session_state.workflow_text, height=300
)

col1, col2 = st.columns(2)
logs_placeholder = st.empty()
preview_placeholder = st.empty()

with col1:
    if st.button("Preview Steps"):
        try:
            data = yaml.safe_load(st.session_state.workflow_text) or {}
            steps = data.get("steps", [])
            preview_placeholder.json(steps)
        except Exception as exc:
            preview_placeholder.error(f"Failed to parse YAML: {exc}")

with col2:
    if st.button("Run Workflow"):
        temp_path = workflow_dir / "__temp.yaml"
        temp_path.write_text(st.session_state.workflow_text)
        buffer = StringIO()
        try:
            with redirect_stdout(buffer):
                run_workflow(temp_path)
        except Exception as exc:
            buffer.write(f"Error: {exc}\n")
        logs_placeholder.text_area("Logs", buffer.getvalue(), height=200)
