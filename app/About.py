import streamlit as st
import numpy as np
import time
from utils.ui_styles import apply_global_styles

st.logo("app/assets/logo_circle.png", size="large")
apply_global_styles()

with st.container(border=False):
    st.image("app/assets/story-vibe-banner.png")
    
with st.container(border=True):
    
    col1, col2 = st.columns([1, 2], vertical_alignment="center")
    
    
    with col1:
        st.markdown("- Upload")
        st.markdown("- Analyse")
        st.markdown("- Inspect")

        st.markdown('''
        <style>
        [data-testid="stMarkdownContainer"] ul{
            list-style-position: inside;
            font-weight: bold;
        }
        </style>
        ''', unsafe_allow_html=True)
          
    with col2:        
        multi = '''
        Upload a txt file from your favorite book.
        
        Our LLM analyzes the text in the granularity of your choice.
        
        Inspect the emotional flow of the story.
        '''
        st.markdown(multi)


