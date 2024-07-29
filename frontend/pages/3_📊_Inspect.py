import streamlit as st
import numpy as np


st.markdown("""
<style>
.title {
    font-size:40px;
    font-weight:bold;
    
}
</style>
""", unsafe_allow_html=True)

st.markdown("<p class=title> Inspect Story</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True, height = 400):
        st.markdown("<p> Segment Slider </p>", unsafe_allow_html=True)
        st.line_chart([0,5, 5,0])
        
with col2:
    with st.container(border=True, height=400):
        st.markdown("<p> Text showcaser: <br> Lorem Impsum e.t.c e.t.c </p>", unsafe_allow_html=True)

st.divider()

with col1:
    with st.container(border=True, height = 400):
        st.markdown("<p> Segmentation Score </p>", unsafe_allow_html=True)
        st.line_chart([0,5, 5,0])
        
with col2:
    with st.container(border=True, height = 400):
        st.markdown("<p> Radar Plot </p>", unsafe_allow_html=True)
        st.line_chart([0,5, 5,0])