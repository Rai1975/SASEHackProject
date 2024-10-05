from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np

model_name = "Minej/bert-base-personality"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def generate_ocean_vector(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    
    # Perform inference and get the model's outputs
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get the raw logits and apply sigmoid to get probabilities (since personality scores range from 0 to 1)
    logits = outputs.logits
    probabilities = torch.sigmoid(logits).squeeze().tolist()
    
    # Convert the probabilities to a simple vector (list)
    ocean_vector = np.array(probabilities)
    
    return ocean_vector