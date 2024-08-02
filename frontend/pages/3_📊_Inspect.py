import streamlit as st

import plotly.express as px
import pandas as pd
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
    st.subheader("Segment Slider:")
    with st.container(border=True, height = 400):
        paragraphs = st.session_state['paragraphs']
        chart_data = pd.DataFrame(np.array([len(p) for p in paragraphs]))
        st.line_chart(chart_data)
        
with col2:
    st.subheader("Inputted text:")
    with st.container(border=True, height=400):
        st.text(st.session_state["text_input"])


with st.container(border=True, height = 400):
    st.markdown("<p> Segmentation Score </p>", unsafe_allow_html=True)
    st.line_chart([0,5, 5,0])
    
with st.container(border=True):
    categories = []
    for sent,value in st.session_state.sentiments.items():
        if value == True:
            categories.append(sent)
            
    values = np.arange(len(categories)) + 1

    # Create a DataFrame
    df = pd.DataFrame({
        'category': categories,
        'value': values
    })
    
    # Create a radar chart
    fig = px.line_polar(df, r='value', theta='category', 
                        line_close=True)
    fig.update_traces(fill='toself')

    # Display the radar chart in Streamlit
    st.plotly_chart(fig)