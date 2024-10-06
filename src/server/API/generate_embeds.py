from transformers import AutoTokenizer, AutoModelForCausalLM
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import numpy as np
import requests

EMBED_URL = "http://100.123.182.40:8000/v1/embeddings"

def pre_processor(open_ans, cons_ans, extr_ans, agre_ans, neuro_ans):
    text = [open_ans, cons_ans, extr_ans, agre_ans, neuro_ans]
    return text

def get_embeds(string):
    # Payload data
    payload = {
        "model": "BAAI/bge-en-icl",  # specify the model you are using
        "input": f"{string}"
    }
    # Make the POST request to the Ollama API
    response = requests.post(EMBED_URL, json=payload)

    # Parse the response
    data = response.json()["data"][0]["embedding"]
    return data

def get_ocean_embeds(Ocean):
    ocean_embeds = []
    for string in Ocean:
        ocean_embeds.append(get_embeds(string))

    return ocean_embeds