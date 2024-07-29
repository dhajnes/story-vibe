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

col1, col2, col3 = st.columns([8,1,3], vertical_alignment="center")

with col1:
    with st.container(border=True, height=250):
        st.markdown("<p> Start writing...</p>", unsafe_allow_html=True)
        
with col2:
    st.markdown("<p> Or </p>", unsafe_allow_html=True)
        
with col3:
    with st.container(border=True):
        col31, col32 = st.columns(2)
        
        with col31:
            st.image('test.jpg')
        
        with col32:
            st.markdown("<p> Upload a .txt file</p>", unsafe_allow_html=True)

col1, col2 = st.columns([4,1],vertical_alignment='center')
with col1:
    st.markdown("<p> Choose Supported Sentiments:</p>", unsafe_allow_html=True)

    option_s = st.checkbox('Neutral (mandatory)')
    option_u = st.checkbox('Sadness')
    option_v = st.checkbox('Happiness')
    option_v = st.checkbox('Fear')
    option_a = st.checkbox('Disgust')
    option_a = st.checkbox('Surprise')
    option_a = st.checkbox('Anger')
    
with col2:
    st.button("Analyse!")