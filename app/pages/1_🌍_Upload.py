import streamlit as st
import numpy as np
import time
import re

st.logo("app/test.jpg")
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
        
    paragraphs = re.split('\n\n|\r\n', text_input)
    paragraphs = [i for i in paragraphs if len(i)>1]
    st.session_state['paragraphs'] = paragraphs

col1, col2 = st.columns([4,1],vertical_alignment='center')

with col1:
    st.markdown("<p> Choose Supported Sentiments:</p>", unsafe_allow_html=True)

    if 'sentiments' not in st.session_state:
        st.session_state.sentiments = {
            'Neutral': True,
            'Sadness': False,
            'Happiness': False,
            'Fear': False,
            'Disgust': False,
            'Surprise': False,
            'Anger': False
        }

    # Display checkboxes and update session state
    st.session_state.sentiments['Neutral'] = st.checkbox('Neutral (mandatory)', value=True, disabled=True)
    st.session_state.sentiments['Sadness'] = st.checkbox('Sadness', value=st.session_state.sentiments['Sadness'])
    st.session_state.sentiments['Happiness'] = st.checkbox('Happiness', value=st.session_state.sentiments['Happiness'])
    st.session_state.sentiments['Fear'] = st.checkbox('Fear', value=st.session_state.sentiments['Fear'])
    st.session_state.sentiments['Disgust'] = st.checkbox('Disgust', value=st.session_state.sentiments['Disgust'])
    st.session_state.sentiments['Surprise'] = st.checkbox('Surprise', value=st.session_state.sentiments['Surprise'])
    st.session_state.sentiments['Anger'] = st.checkbox('Anger', value=st.session_state.sentiments['Anger'])

    # Display the selected sentiments
    st.divider()
    st.write("Selected Sentiments:")
    display_text = "Neutral"
    for sent, active in st.session_state.sentiments.items():
        if active and sent!='Neutral':
            display_text += ", {}".format(sent)
    st.text(display_text)
    
with col2:
    st.button("Analyse!") #Start analysing input or uploaded text
    
st.divider()