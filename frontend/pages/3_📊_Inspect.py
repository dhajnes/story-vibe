import streamlit as st
st.set_page_config(layout="wide")
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
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
    with st.container(border=True):
        if 'paragraphs' in st.session_state:
            paragraphs = st.session_state['paragraphs']
         
            trace =  go.Scatter(
                x=np.arange(len(paragraphs)),
                y=[len(p) for p in paragraphs],
               
                mode='lines+markers',
                marker=dict( 
                    size=10, )
                ,
                selected_marker_color='red')

            # Create the layout
            layout = go.Layout(
                title=None,
                clickmode='event+select'
            )
            
            fig = go.Figure(data=[trace], layout=layout)          
            
            fig.update_layout(showlegend=False)
            fig.update_xaxes(visible=False)
            fig.update_yaxes(visible=False)

            def callback():
                selected_points = st.session_state['chosen_para']['selection']['point_indices']
                if len(selected_points) > 0:
                    para_id = st.session_state['chosen_para']['selection']['point_indices'][0]
                    st.session_state["text_input"] = st.session_state["paragraphs"][para_id]
                
            st.plotly_chart(fig, on_select=callback, key="chosen_para", use_container_width=True)    
             
             
        else:
            st.line_chart()
        
with col2:
    st.subheader("Inputted text:")
    with st.container(border=True, height=450):
        
        if 'text_input' in st.session_state:
            #paragraphs = st.session_state['paragraphs']
            text = st.session_state["text_input"]
            st.text(text)
        else:
            st.text("Lorem Impsum Dolor Sit Amets ...")
        
    
with col1:
    with st.container(border=True):
        
        if 'sentiments' in st.session_state:
            sents = st.session_state.sentiments
            
            nr_of_sents = 0
            categories = []
            for sent,value in st.session_state.sentiments.items():
                if value == True:
                    categories.append(sent)
                    nr_of_sents += 1
                    
            x = np.arange(100) 
            traces = []
            
            for i in range(nr_of_sents):
                y = np.random.randn(100)/2
                traces.append(
                    go.Scatter(
                            x=x, y=y,
                            mode='lines+markers',
                            name=categories[i]
                        )
                    )

            # Create the figure
            fig = go.Figure(data=traces, layout=layout)
            st.plotly_chart(fig)
            
        else:
            st.line_chart()
    
with col2:
    with st.container(border=True):
        if 'sentiments' in st.session_state:
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
        else:
            st.line_chart()