from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoConfig
)
from typing import Union, Literal, Optional, List
from pathlib import Path
import numpy as np
import torch
import nltk

# Download the Punkt tokenizer models
nltk.download('punkt')

current_file = Path(__file__).resolve()
model_path = current_file.parent / "../../data/models/checkpoint-08_07_2024"
MODEL_DIR_PATH = model_path.resolve()

class ModelServing:
    """
    A class to serve a fine-tuned sentiment classification model using HuggingFace Transformers.

    Attributes:
        model_dir_path (Union[str, Path]): Path to the model directory.
        device (torch.device): The PyTorch device to use ('cpu' or 'cuda:0').
        model (PreTrainedModel): The loaded transformer model.
        tokenizer (PreTrainedTokenizer): Tokenizer associated with the model.
        config (PretrainedConfig): Configuration object for the model.
        segments (Optional[List[str]]): Tokenized segments (sentences or paragraphs) of the input text.
        batch_size (int): Number of segments processed per batch.
        segment_type (str): Either 'sentences' or 'paragraphs'.
        all_sentiments (Optional[np.ndarray]): The output sentiment scores.
    """

    def __init__(self, model_dir_path: Union[str, Path], device: Literal["cpu", "cuda:0"]):
        """
        Initializes the ModelServing class and loads the model.

        Args:
            model_dir_path (Union[str, Path]): Path to the model checkpoint directory.
            device (Literal["cpu", "cuda:0"]): Device to run inference on.
        """
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
        """
        Loads the model, tokenizer, and config from the specified directory.
        """

        print(f"[INFO] Loading model from: '{self.model_dir_path}', on the device: '{self.device}'.")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_dir_path)
        self.model.to(self.device)
        self.config = AutoConfig.from_pretrained(self.model_dir_path)
        print(f"Max length: {self.config.max_position_embeddings}")

    def parse_text(
        self,
        segment_type: Literal["sentences", "paragraphs"],
        text: Optional[str] = None,
        source_text_path: Optional[Union[str, Path]] = None
    ) -> List[str]:
        """
        Parses input text into segments based on the specified granularity.

        Args:
            segment_type (Literal["sentences", "paragraphs"]): The unit of text segmentation.
            text (Optional[str]): Raw text to analyze.
            source_text_path (Optional[Union[str, Path]]): File path to load text from.

        Returns:
            List[str]: A list of segmented strings (sentences or paragraphs).
        """
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
            # Normalize line breaks and split
            raw_segments = self.source_text.strip().split('\n\n')
            self.segments = [seg.strip() for seg in raw_segments if seg.strip()]
            
            # Fallback to sentence mode if only one paragraph and it's too short
            if len(self.segments) <= 1:
                print("[INFO] Falling back to sentence mode due to insufficient paragraphs.")
                self.segments = nltk.sent_tokenize(self.source_text)
                self.segment_type = "sentences"
        elif self.segment_type == "sentences":
            self.segments = nltk.sent_tokenize(self.source_text)
        
        return self.segments

    def get_sentiment(self) -> np.ndarray:
        """
        Runs sentiment analysis on previously parsed text segments.

        Returns:
            np.ndarray: An array of shape (n_segments, n_classes) with softmax scores.
        """  
        assert self.segments is not None, (
                    "self.segments is None, first run model.parse_text(segment_type, source_text_path or text)."
                )        
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

    ms = ModelServing(MODEL_DIR_PATH, "cuda:0")
    sample_text = "This is a lovely evening. Isn't it?"
    ms.parse_text("sentences", text=sample_text)
    ms.get_sentiment()
    np.set_printoptions(precision=3, suppress=True)
    print("All sentiments: ", ms.all_sentiments)
        


    

