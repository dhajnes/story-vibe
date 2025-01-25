import streamlit as st
import time
import numpy as np

from backend.analyse_text import ModelServing

# BOOK_PATH = "/home/andrej/Code/story-vibe/data/texts/alice_in_wonderland.txt"
ms = ModelServing("/home/andrej/Code/story-vibe/data/models/checkpoint-08_07_2024",
                    "cuda:0")
# ms.parse_text("sentence", BOOK_PATH)
# ms.get_sentiment()

st.logo("app/test.jpg")
st.title("Analyse Text")
# print("The insides of st.session_state:")
# print(st.session_state)
print(f"st.session_state keys: {list(st.session_state.keys())}")
print(f"[DEBUG] segmenting session state: {st.session_state['segmenting']}")
segment_opt = st.session_state["segmenting"]

with st.empty():
    progress_text = "Analyzing... Please wait."
    progress_bar = st.progress(0, text=progress_text)
    st.session_state[segment_opt] = ms.parse_text(segment_opt, text=st.session_state["text_input"])
    st.session_state["results"] = ms.get_sentiment()
    print(f"st.session_state keys: {list(st.session_state.keys())}")
    print(f"shape of results: {np.shape(st.session_state['results'])}")
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    progress_bar.empty()
    
st.button("Rerun")