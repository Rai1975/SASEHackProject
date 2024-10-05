import numpy as np
from neo4j_db.graph import get_person_embeds, get_person_tags
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

# 0.6x + 0.4y 
def generate_relationship_score(person_id1, person_id2):
    personality_p1 = get_person_embeds(person_id1)["vectorEmbeds"]
    personality_p2 = get_person_embeds(person_id2)["vectorEmbeds"]

    # Computing similarity in personality
    personality_similarity = cosine_similarity(personality_p1, personality_p2)

    p1_tags = get_person_tags(person_id1)
    p2_tags = get_person_tags(person_id2)

    # Computing similarity in tags
    tags_similarity = jaccard_similarity(p1_tags, p2_tags)

    final_score = (0.6 * personality_similarity) + (0.4 * tags_similarity)

    return final_score