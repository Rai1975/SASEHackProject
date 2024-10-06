from transformers import AutoTokenizer, AutoModelForCausalLM
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import numpy as np
import requests

EMBED_URL = "http://100.123.182.40:8000/v1/embeddings"

def cosine_similarity(vector1, vector2):
    # Ensure the input vectors are numpy arrays
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    
    # Compute the dot product of the two vectors
    dot_product = np.dot(vector1, vector2)
    
    # Compute the L2 norms (magnitudes) of the vectors
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    
    # Calculate cosine similarity
    if norm1 == 0 or norm2 == 0:  # Handle zero vector cases
        return 0.0
    else:
        return dot_product / (norm1 * norm2)

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
    for index,string in enumerate(Ocean):
        ocean_embeds.append(get_embeds(string))

    return ocean_embeds