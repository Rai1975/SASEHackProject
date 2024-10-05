import openai
from transformers import AutoTokenizer, AutoModelForCausalLM
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import sys
import os
nltk.download('stopwords')
nltk.download('punkt')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import requests

url = "http://100.126.16.100:8000/v1/embeddings"

def get_embeds(string1):
    tokens1 = word_tokenize(string1.lower())

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens1 = [word for word in tokens1 if word.isalpha() and word not in stop_words]

    # Join tokens back into a string
    filtered_text1 = ' '.join(filtered_tokens1)

    # Payload data
    payload = {
        "model": "BAAI/bge-en-icl",  # specify the model you are using
        "input": f"{filtered_text1}"
    }
    # Make the POST request to the Ollama API
    response = requests.post(url, json=payload)

    # Parse the response
    data1 = response.json()["embedding"]

    return data1
