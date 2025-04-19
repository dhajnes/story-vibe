
import streamlit as st
import time
import numpy as np

from backend.analyse_text import ModelServing
from utils.ui_styles import apply_global_styles

apply_global_styles()

from pathlib import Path

current_file = Path(__file__).resolve()
model_path = current_file.parent / "../../data/models/checkpoint-08_07_2024"
model_path = model_path.resolve()

ms = ModelServing(model_path, "cuda:0")

# UI header
st.logo("app/assets/logo_circle.png", size="large")
st.title("Analyse Text")

# Segmenting method
print(f"st.session_state keys: {list(st.session_state.keys())}")
print(f"[DEBUG] segmenting session state: {st.session_state.get('segmenting')}")
segment_opt = st.session_state.get("segmenting")

# Set model in session
st.session_state["model"] = ms.model
st.session_state["model_labels"] = list(ms.model.config.id2label.values())

# Init flag for rerun
if "rerun_analysis" not in st.session_state:
    st.session_state["rerun_analysis"] = False

# Rerun button
if st.button("🔁 Rerun Analysis"):
    st.session_state["rerun_analysis"] = True
    st.session_state.pop("results", None)

# Run analysis if needed
if "results" not in st.session_state or st.session_state["rerun_analysis"]:

    # Center the GIF using columns
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust ratios if needed
    with col2:
        loading_container = st.empty()
        loading_container.image("app/assets/book_loading.gif", caption="Analyzing...")

    # Perform inference
    segments = ms.parse_text(segment_opt, text=st.session_state["text_input"])
    raw_results = ms.get_sentiment()

    # Post-process with noise
    noise_strength = 0.05
    noise = np.random.normal(loc=0, scale=noise_strength, size=raw_results.shape)
    noisy_results = raw_results + noise
    noisy_results = np.clip(noisy_results, 1e-8, None)
    noisy_results = noisy_results / noisy_results.sum(axis=1, keepdims=True)

    # Store results
    st.session_state["segments"] = segments
    st.session_state["results"] = noisy_results
    st.session_state["model_labels"] = list(ms.model.config.id2label.values())

    # Remove loading GIF
    loading_container.empty()

    # Reset rerun flag
    st.session_state["rerun_analysis"] = False

# Button to go to Inspect
if st.button("Inspect!"):
    st.switch_page("pages/3_📊_Inspect.py")
