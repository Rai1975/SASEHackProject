import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import numpy as np
import requests
import json
def explore_structure(data, indent=0):
    """
    Recursively explore and print the structure of a given data.
    The indent parameter controls the depth level for pretty printing.
    """
    indent_str = "  " * indent  # Create an indentation based on depth

    # Handle numpy arrays
    if isinstance(data, np.ndarray):
        print(f"{indent_str}Type: numpy.ndarray, Shape: {data.shape}, Dtype: {data.dtype}")
    
    # Handle lists
    elif isinstance(data, list):
        print(f"{indent_str}Type: list, Length: {len(data)}")
        if len(data) > 0:
            # Recursively explore first few elements for structure
            for i, item in enumerate(data[:5]):  # Limit to first 5 items for readability
                print(f"{indent_str}  Item {i}:")
                explore_structure(item, indent + 2)
    
    # Handle dictionaries
    elif isinstance(data, dict):
        print(f"{indent_str}Type: dict, Keys: {list(data.keys())}")
        for key, value in data.items():
            print(f"{indent_str}  Key: {key}:")
            explore_structure(value, indent + 2)

    # Handle JSON strings
    elif isinstance(data, str):
        try:
            # Attempt to parse the string as JSON
            parsed_json = json.loads(data)
            print(f"{indent_str}Type: JSON string, Parsed as:")
            explore_structure(parsed_json, indent + 1)
        except json.JSONDecodeError:
            # If it's not valid JSON, treat it as a regular string
            print(f"{indent_str}Type: str, Value: {data}")
    
    # Handle basic types (int, float, etc.)
    elif isinstance(data, (int, float)):
        print(f"{indent_str}Type: {type(data).__name__}, Value: {data}")
    
    # Handle any other types
    else:
        print(f"{indent_str}Type: {type(data).__name__}")


EMBED_URL = "http://100.123.182.40:8000/v1/embeddings"
EMBED_URL = "http://100.123.182.40:8000/encode_text"

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
        temp = get_embeds_fine(string)
        ocean_embeds.append(temp[0])

    return ocean_embeds

def get_embeds_fine(OCEAN_string):
    # Payload data
    payload = {
        'text': OCEAN_string
    }
    # Make the POST request to the Ollama API
    response = requests.get(EMBED_URL, json=payload)

    print(response.json())
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

if __name__=='__main__':
    pass