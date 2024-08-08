import streamlit as st
import time
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

st.logo("test.jpg")
st.title("Analyse Text")

tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

with st.container():
    st.write("Select analyzing granulity:")
    
    st.checkbox("Seperate by paragraphs",value=True,key="use_para")
    
    st.number_input("Set minimum word count:", key="min_size",value=10, step=1, min_value = 0)

if st.button('Analyse'):
    # Initialize the progress bar
    
    if 'text_input' in st.session_state:
        
        paragraphs = re.split('\n\n|\r\n', st.session_state['text_input'])
        paragraphs = [i for i in paragraphs if len(i.split()) > st.session_state['min_size']]
        st.session_state['paragraphs'] = paragraphs
    
        progress_text = "Analyzing... Please wait."
        progress_bar = st.progress(0, text=progress_text)
        progress_bar.empty()
        
        steps = 1/len(paragraphs)
        scores = []
        
        for i,text in enumerate(paragraphs):
            # Progress bar
            progress_bar.progress(i*steps, text=progress_text)
            
            #work being done
            tokens = tokenizer.encode(text, return_tensors='pt')
            result = model(tokens)
            
            scores.append(int(torch.argmax(result.logits))+1)
        
        progress_bar.progress(100, text=progress_text)
        
        st.session_state['scores'] = scores
                
        st.success("Process Completed!")
    else:
        st.write("No text inputted")