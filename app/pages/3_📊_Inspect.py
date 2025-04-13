import streamlit as st
st.set_page_config(layout="wide")
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from utils.ui_styles import apply_global_styles

apply_global_styles()

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
    st.subheader("Segment Overview")
    with st.container(border=True):
        if 'segments' in st.session_state:
            segments = st.session_state['segments']
            char_counts = [len(p) for p in segments]
            x_vals = np.arange(len(segments))

            trace = go.Bar(
                x=x_vals,
                y=char_counts,
                marker=dict(color='rgba(100,150,255,0.8)', line=dict(width=0)),
                hoverinfo='x+y',
            )

            fig = go.Figure(data=[trace])

            fig.update_layout(
                showlegend=False,
                clickmode='event+select',
                xaxis_title="Segment Index",
                yaxis_title="Character Count",
                bargap=0,
                margin=dict(t=20, b=30, l=50, r=20)
            )

            # Optional: add a vertical line for selected segment
            fig.add_vline(
                x=st.session_state['slider_value'],
                line_color="purple",
                line_width=2
            )

            config = {'displayModeBar': False}

            def callback():
                selected_points = st.session_state['chosen_para']['selection']['point_indices']
                if selected_points:
                    para_id = selected_points[0]
                    st.session_state['slider_value'] = para_id
                    st.session_state["text_input"] = st.session_state["segments"][para_id]

            st.plotly_chart(fig, on_select=callback, key="chosen_para", use_container_width=True, config=config)
        else:
            st.line_chart()

        
with col2:
    st.subheader("Chosen text:")

    SEG_RADIUS = 10  # Segments before/after current
    container_height = 600
    with st.container(border=True, height=container_height):
        if "segments" in st.session_state and "text_input" in st.session_state:
            current_idx = st.session_state["slider_value"]
            all_segments = st.session_state["segments"]
            total = len(all_segments)

            scroll_to = f"segment-{current_idx}"  # HTML anchor for scrolling

            html_segments = []
            for offset in range(0, SEG_RADIUS + 1):
                idx = current_idx + offset
                if idx < 0 or idx >= total:
                    continue

                abs_offset = abs(offset)
                alpha = max(0.1, 1.0 - (abs_offset / SEG_RADIUS))  # Smooth fade
                color = f"rgba(255, 255, 255, {alpha:.2f})"
                font_weight = "bold" if offset == 0 else "normal"
                prefix = "👉 **" if offset == 0 else "&nbsp;&nbsp;&nbsp;&nbsp;"
                suffix = "**" if offset == 0 else ""
                anchor = f"id='segment-{idx}'" if offset == 0 else ""
                font_size = 1.25

                # Wrap segment in a paragraph with anchor
                html_segments.append(
                    f"<p {anchor} style='color:{color}; font-weight:{font_weight}; margin-bottom: 1em;'>"
                    f"{prefix}{all_segments[idx]}{suffix}</p>"
                )

            # Combine HTML with scroll target
            html_output = (
                f"<div style='overflow-y: auto; max-height: {container_height};'>"
                f"<a name='{scroll_to}'></a>"
                + "\n".join(html_segments) +
                f"</div>"
            )

            # Inject HTML
            st.markdown(html_output, unsafe_allow_html=True)

with col1:

    col_input, col_btn = st.columns([4, 1])

    with col_input:
        seg_input = st.number_input(
            "Jump to segment:",
            min_value=0,
            max_value=len(st.session_state["segments"]) - 1,
            value=st.session_state["slider_value"],
            step=1,
            key="segment_input"  # DIFFERENT KEY from slider_value
        )

    with col_btn:
        st.markdown("<div style='padding-top: 1.95em;'></div>", unsafe_allow_html=True)

        if st.button("Go!"):
            st.session_state["slider_value"] = st.session_state["segment_input"]

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
    


with col1:
    with st.container(border=True):
        if 'results' in st.session_state and 'model_labels' in st.session_state and 'segments' in st.session_state:
            segments = st.session_state['segments']
            nr_of_segm = len(segments)
            categories = st.session_state['model_labels']
            nr_of_sents = len(categories)

            print(f"[DEBUG] Plotting for {nr_of_segm} segments and {nr_of_sents} sentiment categories")

            x = np.arange(nr_of_segm)
            traces = []

            for i in range(nr_of_sents):
                y = st.session_state["results"][:, i]
                traces.append(
                    go.Scatter(
                        x=x,
                        y=y,
                        mode='lines+markers',
                        name=categories[i]
                    )
                )

            layout = go.Layout(
                title=None,
                clickmode='event+select'
            )

            fig = go.Figure(data=traces, layout=layout)
            fig.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="right",
                    x=1
                )
            )
            fig.add_vline(x=st.session_state['slider_value'], line_color="purple")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No sentiment results available to display.")
    
with col2:
    with st.container(border=True):
        if 'results' in st.session_state:
            # i)   take the pointer from the chosen segment
            # ii)  indice with the pointer into results
            # iii) show the values in a bar chart
            bar_results = st.session_state['results'][st.session_state['slider_value'], :]
            category_list = st.session_state['model_labels']

            # Create a DataFrame
            df = pd.DataFrame({
                'category': category_list,
                'value': bar_results
            })
            print("Dataframe for bar plot:\n")
            print(df)

            # Create a horizontal bar chart
            fig = px.bar(
                df,
                x='category',
                y='value',
                orientation='v',
                range_y=[0, 1],
                labels={'value': 'Score', 'category': 'Sentiment'},
                title="Sentiment Scores",
                
            )

            fig.update_layout(
                yaxis=dict(showgrid=True, gridcolor="LightGray"),
                # xaxis=dict(categoryorder='total ascending'),
                height=500,  # Dynamic height for better spacing
                margin=dict(t=30, l=100, r=30, b=30)
            )

            # Display the bar chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.line_chart()



         