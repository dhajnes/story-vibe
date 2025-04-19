import streamlit as st
import numpy as np
import time
import re
from utils.ui_styles import apply_global_styles

apply_global_styles()

st.logo("app/assets/logo_circle.png", size="large")
st.title("Upload Story")

with st.container(border=True):
    text_input = st.text_area("Temp",label_visibility ="collapsed",placeholder="Start writing...", height=200)
    
    if text_input:
        st.write("Input Processed")
    
st.markdown("<p> Or </p>", unsafe_allow_html=True)
    
with st.container(border=True):
    uploaded_file = st.file_uploader("Upload a .txt file", type="txt")

    if uploaded_file is not None:
        # To read file as string:
        text_input = uploaded_file.read().decode("utf-8")
        
        st.write("File content:")
        
        if len(text_input) > 500:
            st.text(text_input[0:200] + "\n.\n.\n.")
        else:
            st.text(text_input)
    
if text_input:
    st.session_state['text_input'] = text_input

col1, col2 = st.columns([4,1],vertical_alignment='center')

with col1:
    st.markdown("<p> Choose Supported Text Parsing:</p>", unsafe_allow_html=True)
    if 'segmenting' not in st.session_state:
        st.session_state['segmenting'] = "paragraphs"  # Default option

    # Radio button for parsing option
    st.session_state['segmenting'] = st.radio(
        "Parsing Option:",
        options=["paragraphs", "sentences"],
        index=0 if st.session_state['segmenting'] == "paragraphs" else 1,
        help="Choose whether to parse text into paragraphs or sentences."
    )

    st.markdown("<p> Supported Sentiments:</p>", unsafe_allow_html=True)

    supported_sentiments = ['Neutral', 'Sadness', 'Happiness', 'Fear', 'Disgust', 'Surprise', 'Anger']
    for sentiment in supported_sentiments:
        st.markdown(f"• {sentiment}")
    
with col2:
    if st.button("Analyse!"):
        if 'text_input' in st.session_state and len(st.session_state['text_input'].strip()) > 0:
            st.switch_page("pages/2_📈_Analyse.py")
        else:
            st.warning("Please provide some input text first.")
    
st.divider()