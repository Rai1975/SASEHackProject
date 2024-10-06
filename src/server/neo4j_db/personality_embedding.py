from transformers import AutoModelForSequenceClassification, AutoTokenizer
from sentence_transformers import SentenceTransformer
import torch
import numpy as np

embedding_model = SentenceTransformer('all-mpnet-base-v2')

def generate_ocean_vector(text):
    # Generate the embedding vector for the input text
    ocean_vector = embedding_model.encode(text)
    return ocean_vector


def pre_processor(open_ans, cons_ans, extr_ans, agre_ans, neuro_ans):
    text = f"{open_ans} {cons_ans} {extr_ans} {agre_ans} {neuro_ans}"
    return text