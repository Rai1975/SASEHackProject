from transformers import AutoTokenizer, AutoModelForCausalLM
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import numpy as np
import requests

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

EMBED_URL = "http://100.123.182.40:8000/v1/embeddings"
OLLAMA_URL = "http://100.123.182.40:11434/api/generate"

def get_embeds(string1):
    # Payload data
    payload = {
        "model": "BAAI/bge-en-icl",  # specify the model you are using
        "input": f"{string1}"
    }
    # Make the POST request to the Ollama API
    response = requests.post(EMBED_URL, json=payload)

    # Parse the response
    data1 = response.json()["data"][0]["embedding"]
    return data1

def get_ocean_embeds(Ocean):
    ocean_embeds = []
    for string in Ocean:
        ocean_embeds.append(get_embeds(string))

    return ocean_embeds

#string1 = """
# I love exploring new ideas and experiences, always eager to try something different. I plan carefully and stick to my schedules to achieve my goals efficiently.
# Being around people energizes me, and I thrive in social settings. I am considerate of others and strive to maintain harmony in my relationships.
# I remain calm and composed, even in stressful situations."""

string1_O = "I love exploring new ideas and experiences, always eager to try something different." 
string1_C = "I plan carefully and stick to my schedules to achieve my goals efficiently."
string1_E = "Being around people energizes me, and I thrive in social settings."
string1_A = "I am considerate of others and strive to maintain harmony in my relationships."
string1_N = "I remain calm and composed, even in stressful situations."

string1 = [string1_O, string1_C, string1_E, string1_A, string1_N]

string2_O = "I feel uneasy about trying new things and prefer the familiar."
string2_C = "I often leave tasks unfinished and get easily distracted."
string2_E = "I prefer solitude and quiet environments."
string2_A = "I focus on my goals and can be unyielding."
string2_N = "I frequently feel anxious and struggle to cope with stress."

string2 = [string2_O, string2_C, string2_E, string2_A, string2_N]

string3 = sentences = [
    "I prefer to stick with what I know and avoid surprises.",
    "I often act on impulse without much planning.",
    "I feel drained after social interactions and need time alone to recharge.",
    "I often put my interests first and can be critical.",
    "I get stressed easily and find it hard to relax."
]

str1_embed = get_ocean_embeds(string1)
str2_embed = get_ocean_embeds(string2)
str3_embed = get_ocean_embeds(string3)

arr = []
arr2 = []
arr3 = []
for i in range(len(str2_embed)):
    arr.append(cosine_similarity(str1_embed[i], str2_embed[i]))

for i in range(len(str2_embed)):
    arr2.append(cosine_similarity(str2_embed[i], str3_embed[i]))

for i in range(len(str2_embed)):
    arr3.append(cosine_similarity(str1_embed[i], str3_embed[i]))

print(arr)
print(sum(arr)/5)
print()
print(arr2)
print(sum(arr2)/5)
print()
print(arr3)
print(sum(arr3)/5)