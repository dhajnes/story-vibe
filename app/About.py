import streamlit as st
import numpy as np
import time

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
st.logo("app/test.jpg")

with st.container(border=True):
    last_rows = np.random.randn(1, 1)
    col1, col2, col3 = st.columns([1, 1, 3], vertical_alignment="center")
    
    with col1:
        with st.container(border=True):
            st.image("app/test.jpg")
        
    with col2:
        st.markdown("*Lorem* ipsum **dolor** ***sit amet***.")
        
    with col3:
        chart = st.line_chart(last_rows)

with st.container(border=True):
    
    col1, col2 = st.columns([1, 2], vertical_alignment="center")
    
    
    with col1:
        st.markdown("- Upload")
        st.markdown("- Analyze")
        st.markdown("- Interpret")

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

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    #progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")