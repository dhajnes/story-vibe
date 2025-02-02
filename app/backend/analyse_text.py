from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoConfig
)
import torch
from bs4 import BeautifulSoup
from typing import Union, Literal, List

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import nltk
import time
from pathlib import Path

# Download the Punkt tokenizer models
nltk.download('punkt')


MODEL_DIR_PATH = "/home/andrej/Code/story-vibe/data/models/checkpoint-08_07_2024"

class ModelServing:
    def __init__(self, model_dir_path, device: Literal["cpu", "cuda:0"]):
        self.model_dir_path = model_dir_path
        self.device = torch.device(device)
        self.device_str = device
        self.model = None
        self.tokenizer = None
        self.config = None
        self.segments = None
        self.batch_size = None
        self.batch_map = {"cpu":{"sentences":4, "paragraphs":2},    # TODO this is hosting dependent
                          "cuda:0":{"sentences":8, "paragraphs":4}}
        self._load_model()

    def _load_model(self) -> None:
        print(f"[INFO] Loading model from: '{self.model_dir_path}', on the device: '{self.device}'.")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_dir_path)
        self.model.to(self.device)
        self.config = AutoConfig.from_pretrained(self.model_dir_path)
        print(f"Max length: {self.config.max_position_embeddings}")

    # TODO maybe this should return parsed text
    def parse_text(self, segment_type: Literal["sentences", "paragraphs"], text: str = None,
                   source_text_path: Union[str, Path] = None) -> None:
        assert (text is None) != (source_text_path is None), (
        "Either 'text' or 'source_text_path' must be provided, but not both.")

        self.segment_type = segment_type
        self.batch_size = self.batch_map[self.device_str][self.segment_type]
        if source_text_path is not None:
            with open(source_text_path, 'r') as file:
                self.source_text = file.read()
        else:
            self.source_text = text
        
        if self.segment_type == "paragraphs":
            self.segments = self.source_text.split('\n\n')
        elif self.segment_type == "sentences":
            self.segments = nltk.sent_tokenize(self.source_text)
        
        return self.segments

    # TODO typehint this
    def get_sentiment(self):  
        assert self.segments is not None, "self.segments is None, first run model.parse_text(segment_type, source_text_path)."
        
        self.all_sentiments = []
        
        for i in range(0, len(self.segments), self.batch_size):
            batch = self.segments[i:i + self.batch_size]
            inputs = self.tokenizer(batch, return_tensors='pt', truncation=True, padding=True)
            inputs = {key: value.to(self.device) for key, value in inputs.items()}
            if len(inputs['input_ids'][0]) > 350:
                print(f"Input length is larger than 350: {len(inputs['input_ids'][0])}")

            with torch.no_grad():
                outputs = self.model(**inputs)
            scores = outputs.logits.softmax(dim=-1).cpu().numpy()

            self.all_sentiments.extend(scores)
        
        self.all_sentiments = np.array(self.all_sentiments)
        return self.all_sentiments


if __name__ == "__main__":
    BOOK_PATH = "/home/andrej/Code/story-vibe/data/texts/alice_in_wonderland.txt"

    ms = ModelServing("/home/andrej/Code/story-vibe/data/models/checkpoint-08_07_2024",
                      "cuda:0")
    sample_text = "This is a lovely evening. Isn't it?"
    # ms.parse_text("sentences", BOOK_PATH)
    ms.parse_text("sentences", text=sample_text)
    ms.get_sentiment()
    np.set_printoptions(precision=3, suppress=True)
    print("All sentiments: ", ms.all_sentiments)
        


    

