import streamlit as st
import numpy as np
import time

st.markdown("""
<style>
.title {
    font-size:40px;
    font-weight:bold;
    
}
</style>
""", unsafe_allow_html=True)

st.markdown("<p class=title> Upload Story</p>", unsafe_allow_html=True)

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
        

col1, col2 = st.columns([4,1],vertical_alignment='center')

with col1:
    st.markdown("<p> Choose Supported Sentiments:</p>", unsafe_allow_html=True)

    neutral = st.checkbox('Neutral (mandatory)', value=True, disabled=True)
    sadness = st.checkbox('Sadness')
    happiness = st.checkbox('Happiness')
    fear = st.checkbox('Fear')
    disgust = st.checkbox('Disgust')
    surprise = st.checkbox('Surprise')
    anger = st.checkbox('Anger')
    
    # Collect selected sentiments
    selected_sentiments = ['Neutral']
    if sadness:
        selected_sentiments.append('Sadness')
    if happiness:
        selected_sentiments.append('Happiness')
    if fear:
        selected_sentiments.append('Fear')
    if disgust:
        selected_sentiments.append('Disgust')
    if surprise:
        selected_sentiments.append('Surprise')
    if anger:
        selected_sentiments.append('Anger')

    # Display the selected sentiments
    st.write("Selected Sentiments:")
    st.text(", ".join(selected_sentiments) if len(selected_sentiments) > 1 else "None")
    
with col2:
    st.button("Analyse!") #Start analysing input or uploaded text