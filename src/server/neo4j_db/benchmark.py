from transformers import AutoTokenizer, AutoModelForCausalLM
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import numpy as np
import requests


EMBED_URL = "http://100.123.182.40:8000/encode_text"
EMBED_URL = "http://100.123.182.40:8000/v1/embeddings"

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

def get_embeds_fine(OCEAN_string):
    # Payload data
    payload = {
        'text': OCEAN_string
    }
    # Make the POST request to the Ollama API
    response = requests.get(EMBED_URL, json=payload)

    # Parse the response
    data = response.json()["encoded"]
    return data

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

skibidi1 = ["I love exploring new ideas and experiences, always eager to try something different.",
    "I plan carefully and stick to my schedules to achieve my goals efficiently.",
    "Being around people energizes me, and I thrive in social settings.",
    "I am considerate of others and strive to maintain harmony in my relationships.",
    "I remain calm and composed, even in stressful situations."
]

skibidi2 = [
    "I feel uneasy about trying new things and prefer the familiar.",
    "I often leave tasks unfinished and get easily distracted.",
    "I prefer solitude and quiet environments.",
    "I focus on my goals and can be unyielding.",
    "I frequently feel anxious and struggle to cope with stress."
]

skibidi3 = [
    "I prefer to stick with what I know and avoid surprises",
    "I often act on impulse without much planning.",
    "I feel drained after social interactions and need time alone to recharge",
    "I often put my interests first and can be critical",
    "I get stressed easily and find it hard to relax."
]


sk1 = get_ocean_embeds(skibidi1)
sk2 = get_ocean_embeds(skibidi2)
sk3 = get_ocean_embeds(skibidi3)

skhm = []
skhm2 = []
skhm3 = []

for i in range(len(sk2)):
    skhm3.append(cosine_similarity(sk1[i], sk2[i]))

for i in range(len(sk2)):
    skhm.append(cosine_similarity(sk2[i], sk3[i]))

for i in range(len(sk2)):
    skhm2.append(cosine_similarity(sk1[i], sk3[i]))

print(skhm3)
print(sum(skhm3)/5)
print(skhm)
print(sum(skhm)/5)
print(skhm2)
print(sum(skhm2)/5)
