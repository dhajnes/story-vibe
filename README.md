<p align="center">
  <img src="imgsrc/story-vibe-banner.png" alt="Visualize and quantify the vibe of any story.">
</p>

# Instantly analyse and understand the emotional tone of any story.
This repository includes complete scripts on finetuning BERT - **Bidirectional Encoder Representations from Transformers** to output sentiment analysis. We trained BERT on Google's GoEmotions dataset collected from Reddit's annotators. See Google's [blog](https://research.google/blog/goemotions-a-dataset-for-fine-grained-emotion-classification/) about GoEmotions.

1. Dataset is available for download on Kaggle [here](https://www.kaggle.com/datasets/debarshichanda/goemotions).
2. model weights are available on my Model Card on HuggingFace [here](https://huggingface.co/dhajnes/bert-story-vibe/tree/main).
3. Having fun with the model inference is mandatory.
4. Live deployment ... maybe ... TBA


The script is powered by `Streamlit` a front-end Python library.

# Demo
<p align="center">
  <img src="imgsrc/story-vibe-tutorial.gif" alt="Example of running Story-vibe.">
</p>

## Contributors ✨

<!-- ALL-CONTRIBUTORS-LIST:START -->
<!-- prettier-ignore -->
<table>
<tr><td align="center"><a href="https://github.com/dhajnes"><img src="https://avatars.githubusercontent.com/dhajnes" width="100px;" alt=""/><br /><sub><b>Andrej Kružliak</b></sub></a></td>
<td align="center"><a href="https://github.com/johmag2"><img src="https://avatars.githubusercontent.com/johmag2" width="100px;" alt=""/><br /><sub><b>Johan Magnusson</b></sub></a></td>
</tr>
</table>
<!-- ALL-CONTRIBUTORS-LIST:END -->

# Install
1. install and activate the conda environment in `/install/conda_environment.yaml` via `conda env create -f /install/conda_environment.yaml`
2. download the model checkpoint (including training params and optimizer weights) from my HuggingFace [here](https://huggingface.co/dhajnes/bert-story-vibe/tree/main)
3. deploy locally via `streamlit run app/About.py`
   

# Train yourself
- See folder `/source`
  - includes `bert_run.ipynb` and `bert_train.ipynb`
  - follow the structure of the jupyter notebook

# Additional notes
- the dataset GoEmotions includes roughly 30% of misslabelings because of native vs non-native understanding of english
- the internal benchmark accuracy is roughly 63%, evaluated on `data/texts/emotions_dataset_personal_eval.csv`
- GPT4 and GPT4o are both great at hipfiring the sentiment guesses 0-shot and 1-shot, this BERT training is just seeing whether we could, not whether we should