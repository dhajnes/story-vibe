import streamlit as st
st.set_page_config(layout="wide")
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

st.logo("test.jpg")
st.title("Inspect Story")

if 'paragraphs' not in st.session_state:
    st.session_state['paragraphs'] = []

##Markdown styles
st.markdown(
    """
    <style>
    .stSlider > div {
        width: 95%;  /* Adjust this value to change the slider width */
        margin: auto;  /* Center the slider */
    }
    .stIndex > div {
        margin: auto;  /* Center the slider */
    }
    </style>
    """,
    unsafe_allow_html=True
)

if 'analysed' in st.session_state and st.session_state['analysed']:
        
    col1, col2 = st.columns([3,2], vertical_alignment='center')

    with col1:
        st.subheader("Segment Slider:")
        with st.container(border=True):
            if 'paragraphs' in st.session_state:
                paragraphs = st.session_state['paragraphs']
            
                trace =  go.Scatter(
                    x=np.arange(len(paragraphs)),
                    y=[len(p.split()) for p in paragraphs],
                
                    mode='lines',
                    marker=dict( 
                        size=10, )
                    ,
                    selected_marker_color='red')

                # Create the layout
                layout = go.Layout(
                    title=None,
                    clickmode='event+select'
                )
                
                config = {'displayModeBar': False}
                
                fig = go.Figure(data=[trace])          
                
                fig.update_layout(showlegend=False)
                fig.update_xaxes(visible=True)
                fig.update_yaxes(visible=True)

                def callback():
                    selected_points = st.session_state['chosen_para']['selection']['point_indices']
                    if len(selected_points) > 0:
                        para_id = st.session_state['chosen_para']['selection']['point_indices'][0]
                        st.session_state['slider_value'] = para_id
                        st.session_state["text_input"] = st.session_state["paragraphs"][para_id]
                    
                if 'slider_value' in st.session_state:
                    x=st.session_state['slider_value']
                else:
                    x = 0
                fig.add_vline(x=x,line_width=3,line_color="purple")
                
                for i in st.session_state['chapter_indicies']:
                    fig.add_vline(x=i,line_width=0.5,line_color="black",line_dash="dash")
                    
                
                st.plotly_chart(fig, on_select=callback, key="chosen_para",
                                use_container_width=True, config=config)    
                
                
            else:
                st.line_chart()
            
    with col2:
        st.subheader("Selected Text:")
        with st.container(border=True, height=400):
            
            if 'paragraphs' in st.session_state and len(paragraphs)>0:
                if 'slider_value' in st.session_state:
                    st.write(st.session_state["paragraphs"][st.session_state['slider_value']])
                else:
                    st.write(st.session_state["paragraphs"][0])
                    
            elif 'text_input' in st.session_state:               
                st.write(st.session_state["text_input"])
            else:
                st.text("Lorem Impsum Dolor Sit Amets ...")
        
        if 'slider_value' in st.session_state:
            st.write("Segment {}/{}".format(st.session_state['slider_value'],len(st.session_state["paragraphs"])))
        
            if 'scores' in st.session_state:
                st.write("Bert Sentiment Score: {}".format(st.session_state['scores'][st.session_state['slider_value']]))
        else:
            st.write("Segment {}/{}".format(0,len(st.session_state["paragraphs"])))
        
            if 'scores' in st.session_state:
                st.write("Bert Sentiment Score: {}".format(st.session_state['scores'][0]))

    with col1:
        col11, col12 = st.columns([9,1])
        if 'paragraphs' in st.session_state:
            def slider_update():
                st.session_state['input_value'] = st.session_state['slider_value'] 
                if st.session_state['slider_value'] >= 0 and len(st.session_state["paragraphs"])>0:
                    paragraphs = st.session_state["paragraphs"]
            
            def input_update():
                st.session_state['slider_value'] = st.session_state['input_value']
                if st.session_state['slider_value'] >= 0 and len(st.session_state["paragraphs"])>0:
                    paragraphs = st.session_state["paragraphs"]
            
            with col11:
                selected_value = st.slider(
                    label="Select Segment:",
                    min_value=0,  # Minimum value of the slider
                    max_value= max(len(st.session_state['paragraphs'])-1,1),  # Maximum value of the slider
                    value=0,  # Default value (optional)
                    key='slider_value',
                    on_change=slider_update
                )
            
            with col12:
                st.number_input(
                    label="temp",
                    label_visibility = 'hidden',
                    min_value=0,  # Minimum value of the slider
                    max_value= max(len(st.session_state['paragraphs'])-1,1),  # Maximum value of the slider
                    value=0,
                    key='input_value',
                    on_change=input_update
                )
        else:
            st.slider(label="Select paragraph",
                min_value=0,  # Minimum value of the slider
                max_value=1  # Maximum value of the slider
            )

    col1, col2 = st.columns([3,2],vertical_alignment='center')

    with col1:
        with st.container(border=True):
            st.toggle("Bert",key="toggle_value")
            
            if 'sentiments' in st.session_state:
                sents = st.session_state.sentiments
                if 'paragraphs' in  st.session_state:
                    nr_of_para = len(st.session_state['paragraphs'])
                else:
                    nr_of_para = 1
                
                nr_of_sents = 0
                categories = []
                for sent,value in st.session_state.sentiments.items():
                    if value == True:
                        categories.append(sent)
                        nr_of_sents += 1
                        
                x = np.arange(nr_of_para) 
                traces = []
                
                # Create the layout
                layout = go.Layout(
                    title=None,
                    clickmode='event+select'
                )
                
                
                if not st.session_state['toggle_value']:
                        
                    for i in range(nr_of_sents):
                        y = np.random.randn(nr_of_para)
                        traces.append(
                            go.Scatter(
                                    x=x, y=y,
                                    mode='lines',
                                    name=categories[i]
                                )
                            )
                else:
                    y = st.session_state['scores']
                    traces.append(
                        go.Scatter(
                                x=x, y=y,
                                mode='lines'
                            )
                        )
                    
                # Create the figure
                fig = go.Figure(data=traces, layout=layout)
                fig.update_layout(legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="right",
                    x=1
                ))
                
                fig.add_vline(x=st.session_state['slider_value'],line_width=3,line_color="purple")
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
                
                fig.update_layout(
                    margin=dict(l=50, r=50, t=20, b=20)
                )
                fig.update_traces(fill='toself')
                
                # Display the radar chart in Streamlit
                st.plotly_chart(fig)
            else:
                st.line_chart()
else:
    st.header("Perform Analysing First")