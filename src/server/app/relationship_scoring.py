import numpy as np
from server.app.personality_embedding import generate_ocean_vector

def jaccard_similarity(tags1, tags2):
    # Combine both tag lists to get unique tags
    unique_tags = set(tags1).union(set(tags2))
    
    # Create binary arrays for each tag list
    binary_tags1 = np.array([1 if tag in tags1 else 0 for tag in unique_tags])
    binary_tags2 = np.array([1 if tag in tags2 else 0 for tag in unique_tags])
    
    # Compute intersection and union
    intersection = np.sum(np.logical_and(binary_tags1, binary_tags2))
    union = np.sum(np.logical_or(binary_tags1, binary_tags2))
    
    return intersection / union if union != 0 else 0

# 0.6x + 0.4y 
def generate_relationship_score(person1, person2):
    pass