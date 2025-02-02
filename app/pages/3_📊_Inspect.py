import streamlit as st
st.set_page_config(layout="wide")
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

st.logo("app/test.jpg")
st.title("Inspect Story")

##Init base session_state variables
if 'slider_value' not in st.session_state:
    st.session_state['slider_value'] = 0

##Markdown styles
st.markdown(
    """
    <style>
    .stSlider > div {
        width: 85%;  /* Adjust this value to change the slider width */
        margin: auto;  /* Center the slider */
    }
    </style>
    """,
    unsafe_allow_html=True
)

    
col1, col2 = st.columns([3,2])

with col1:
    st.subheader("Segment Slider:")
    with st.container(border=True):
        if 'segments' in st.session_state:
            segments = st.session_state['segments']
         
            trace =  go.Scatter(
                x=np.arange(len(segments)),
                y=[len(p) for p in segments],
               
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
            
            config = {'displayModeBar': False}
            
            fig = go.Figure(data=[trace],)          
            
            fig.update_layout(showlegend=False)
            fig.update_xaxes(visible=True)
            fig.update_yaxes(visible=True)

            def callback():
                selected_points = st.session_state['chosen_para']['selection']['point_indices']
                if len(selected_points) > 0:
                    para_id = st.session_state['chosen_para']['selection']['point_indices'][0]
                    st.session_state['slider_value'] = para_id
                    st.session_state["text_input"] = st.session_state["segments"][para_id]
                
            fig.add_vline(x=st.session_state['slider_value'],line_color="purple")
            
            st.plotly_chart(fig, on_select=callback, key="chosen_para",
                            use_container_width=True, config=config)    
             
             
        else:
            st.line_chart()
        
with col2:
    st.subheader("Chosen text:")
    with st.container(border=True, height=400):
        
        if 'text_input' and "segments" in st.session_state:
            #segments = st.session_state['segments']
            # text = st.session_state["text_input"]
            text_part = st.session_state["segments"][st.session_state['slider_value']]
            st.write(text_part)
        else:
            st.text("Lorem Impsum Dolor Sit Amets ...")

with col1:
        if 'segments' in st.session_state:
            def slider_update():
                if st.session_state['slider_value'] >= 0 and len(st.session_state["segments"])>0:
                    segments = st.session_state["segments"]
                    st.session_state["text_input"] = segments[st.session_state['slider_value']]
            
                
            selected_value = st.slider(
                label="Select segment",
                min_value=[-1 if  len(st.session_state['segments'])==0 else 0][0],  # Minimum value of the slider
                max_value= len(st.session_state['segments'])-1,  # Maximum value of the slider
                value=st.session_state['slider_value'],  # Default value (optional)
                key='slider_value',
                on_change=slider_update
            )
        else:
            st.slider(label="Select segment",
                min_value=0,  # Minimum value of the slider
                max_value=1  # Maximum value of the slider
            )

col1, col2 = st.columns([3,2])

with col1:
    with st.container(border=True):
        
        if 'sentiments' in st.session_state:
            sents = st.session_state.sentiments
            if 'segmenting' in  st.session_state:
                segm_option = st.session_state['segmenting']
                print(type(st.session_state["segments"]))
                print(len(st.session_state["segments"]))
                nr_of_segm = len(st.session_state["segments"])
            else:
                nr_of_segm = 1

            print(f"[DEBUG] nr_of_segm: {nr_of_segm}")
            # print(f"st.session_state['segments'].shape: {st.session_state['segments'].shape}")
            
            nr_of_sents = 0
            categories = []
            for sent,value in st.session_state.sentiments.items():
                if value == True:
                    categories.append(sent)
                    # TODO FIXME for now, only full range of labels available
                    nr_of_sents += 1
            
            categories = st.session_state.model_labels
            nr_of_sents = len(categories)
                    
            x = np.arange(nr_of_segm) 
            traces = []
            
            # Create the layout
            layout = go.Layout(
                title=None,
                clickmode='event+select'
            )
            
            for i in range(nr_of_sents):
                # y = np.random.randn(nr_of_segm)
                y = st.session_state["results"][:,i]
                traces.append(
                    go.Scatter(
                            x=x, y=y,
                            mode='lines+markers',
                            name=categories[i]
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
            
            fig.add_vline(x=st.session_state['slider_value'],line_color="purple")
            st.plotly_chart(fig)
            
        else:
            st.line_chart()
    
with col2:
    with st.container(border=True):
        if 'results' in st.session_state:
            # i)   take the pointer from the chosen segment
            # ii)  indice with the pointer into results
            # iii) show the values in the radar plot
            radar_results = st.session_state['results'][st.session_state['slider_value'], :]
            category_list = st.session_state['model_labels']
            

            # categories = []
            # for sent,value in st.session_state.sentiments.items():
            #     if value == True:
            #         categories.append(sent)
                    
            # values = np.arange(len(categories)) + 1

            # Create a DataFrame
            df = pd.DataFrame({
                'category': category_list,
                'value': radar_results
            })
            
            # Create a radar chart
            fig = px.line_polar(df, r='value', theta='category', 
                                line_close=True)
            fig.update_traces(fill='toself')
            
            # Display the radar chart in Streamlit
            st.plotly_chart(fig)
        else:
            st.line_chart()