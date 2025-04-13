import streamlit as st

def apply_global_styles():
    st.markdown(
        """
        <style>
        html, body, [class*="css"]  {
            font-size: 1.15em !important;
        }
        .stSlider > div {
            font-size: 1.15em !important;
        }
        .stTextInput input, .stNumberInput input {
            font-size: 1.0em !important;
        }
        .stButton > button {
            font-size: 1.05em !important;
        }
        .stRadio label, .stCheckbox label {
            font-size: 1.05em !important;
        }
        .stPlotlyChart {
            font-size: 1.05em !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )