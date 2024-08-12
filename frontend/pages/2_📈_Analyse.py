import streamlit as st
import time
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

st.logo("test.jpg")
st.title("Analyse Text")

tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')


if "text_input" in st.session_state:

    with st.container():
        st.write("Select analyzing granulity:")
        option = st.selectbox(
            "Select how to seperate the segments:",
            ("Paragraphs", "Sentences", "Words"),
            placeholder="Select seperation method...",
        )
        
        if option == "Paragraphs":
            st.number_input("Minimum words per paragraph",  key="min_size",value=10, step=1, min_value = 0)
        
        elif option == "Sentences":
            st.number_input("How many sentences per segment:",key="sentences_buffer",value=10, step=1, min_value = 0)
         
        elif option == "Words":
            st.number_input("How many words per segment:",key="word_buffer",value=10, step=1, min_value = 0)
        
        else:
            pass
        
        analyze = st.button("Analyse")
        if analyze:
            # Initialize the progress bar
            chapter_indicies = []
                
            if option == "Paragraphs":
                paragraphs = re.split('\n\n|\r\n', st.session_state['text_input'])
                #paragraphs = [i for i in paragraphs if len(i)>0] ##Remove empty
                paragraphs = [i for i in paragraphs if len(i.split()) > st.session_state['min_size'] or 'chapter' in i.lower()]
                chapter_indicies = [i for i,j in enumerate(paragraphs) if 'chapter' in j.lower()]
                                
            elif option == "Sentences":
                paragraphs =  re.split(r'(?<=[.!?])\s+', st.session_state['text_input'])
                paragraphs = [i for i in paragraphs if len(i)>0] ##Remove empty
                
            elif option == "Words":
                paragraphs = st.session_state['text_input'].split()
                paragraphs = [i for i in paragraphs if len(i)>0] ##Remove empty
                                
            else:
                pass
                          
            if option == "Sentences":
                new_para = []
                buffer = st.session_state['sentences_buffer']
                    
                for i in range(len(paragraphs)//buffer):
                    try:
                        text = ' '.join(paragraphs[i*buffer:(i+1)*buffer])
                    except:
                        text = ' '.join(paragraphs[i*buffer:])
                        
                    new_para.append(text)
                        
                paragraphs = new_para                
                chapter_indicies = [i for i,j in enumerate(paragraphs) if 'chapter' in j.lower()]
                
            elif option == "Words":
                new_para = []
                buffer = st.session_state['word_buffer']
                    
                for i in range(len(paragraphs)//buffer):
                    try:
                        text = ' '.join(paragraphs[i*buffer:(i+1)*buffer])
                    except:
                        text = ' '.join(paragraphs[i*buffer:])
                        
                    new_para.append(text)
                        
                paragraphs = new_para
                chapter_indicies = [i for i,j in enumerate(paragraphs) if 'chapter' in j.lower()]
            
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
            st.session_state['chapter_indicies'] = chapter_indicies
                    
            st.success("Process Completed!")
            st.session_state['analysed'] = True
        
else:
    st.header("No text inputted")