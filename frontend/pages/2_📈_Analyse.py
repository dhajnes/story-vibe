import streamlit as st
import time

st.markdown("""
<style>
.title {
    font-size:40px;
    font-weight:bold;
    
}
</style>
""", unsafe_allow_html=True)

st.markdown("<p class=title> Analyse Text</p>", unsafe_allow_html=True)

with st.empty():
    progress_text = "Analyzing... Please wait."
    progress_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    progress_bar.empty()
    
st.button("Rerun")