import numpy as np
from heapq import heappop, heappush
from neo4j_db.graph import init_driver
from neo4j_db.CRUD import get_person_embeds, get_person_tags
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from classes.person import Person

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


def filter_friends(potential_friends, ptags):
    person_tags = ptags
    heap = []  

    for p in potential_friends:
        try:
            # Access the OCEAN similarity values from the dictionary
            print(p)
            O = p["O_similarity"]
            C = p["C_similarity"]
            E = p["E_similarity"]
            A = p["A_similarity"]
            N = p["N_similarity"]
            
            # Calculate the average similarity score
            avg_sim_score_vector = (O + C + E + A + N) / 5
            print(avg_sim_score_vector)
        except Exception as e:
            print(f"Error processing embeddings for person ID {p['pid']}: {e}")
            continue  

        # Generate the relationship score based on vector and tag similarity
        score = generate_relationship_score(avg_sim_score_vector, person_tags, p['tags'])

        # Use negative score to simulate a max-heap since heapq is a min-heap
        heappush(heap, (-score, (p['pid'], p['name'], p.get('age', 'N/A'), score)))

    # Prepare the list to return top N friends based on the score
    return_list = []
    num_friends_to_return = min(5, len(heap))  # Ensure we don't pop more than available

    for _ in range(num_friends_to_return):
        # heappop returns a tuple: (-score, (pid, name, age, score))
        _, friend_info = heappop(heap)
        return_list.append(friend_info)

    return return_list
    

# Lord forgive me
def generate_relationship_score(vector_sim_score, tags1, tags2):
    return 0.6*(vector_sim_score) + 0.4*(jaccard_similarity(tags1, tags2))

# Finding Potential friends for the user
def find_potential_friends(person_id):
    person_embeds = get_person_embeds(person_id)
    
    query = """
    WITH $p_O_embed AS query_O_vector, 
         $p_C_embed AS query_C_vector, 
         $p_E_embed AS query_E_vector, 
         $p_A_embed AS query_A_vector, 
         $p_N_embed AS query_N_vector
    MATCH (p:Person)
    WITH p, query_O_vector, query_C_vector, query_E_vector, query_A_vector, query_N_vector, 
         p.O_embed AS person_O_vector, 
         p.C_embed AS person_C_vector, 
         p.E_embed AS person_E_vector, 
         p.A_embed AS person_A_vector, 
         p.N_embed AS person_N_vector
    WITH p, 
         REDUCE(sum = 0.0, i IN RANGE(0, SIZE(query_O_vector)-1) | sum + query_O_vector[i] * person_O_vector[i]) AS O_dotProduct,
         REDUCE(sum = 0.0, i IN RANGE(0, SIZE(query_C_vector)-1) | sum + query_C_vector[i] * person_C_vector[i]) AS C_dotProduct,
         REDUCE(sum = 0.0, i IN RANGE(0, SIZE(query_E_vector)-1) | sum + query_E_vector[i] * person_E_vector[i]) AS E_dotProduct,
         REDUCE(sum = 0.0, i IN RANGE(0, SIZE(query_A_vector)-1) | sum + query_A_vector[i] * person_A_vector[i]) AS A_dotProduct,
         REDUCE(sum = 0.0, i IN RANGE(0, SIZE(query_N_vector)-1) | sum + query_N_vector[i] * person_N_vector[i]) AS N_dotProduct,
         SQRT(REDUCE(sum = 0.0, i IN RANGE(0, SIZE(person_O_vector)-1) | sum + person_O_vector[i]^2)) AS O_personMagnitude,
         SQRT(REDUCE(sum = 0.0, i IN RANGE(0, SIZE(person_C_vector)-1) | sum + person_C_vector[i]^2)) AS C_personMagnitude,
         SQRT(REDUCE(sum = 0.0, i IN RANGE(0, SIZE(person_E_vector)-1) | sum + person_E_vector[i]^2)) AS E_personMagnitude,
         SQRT(REDUCE(sum = 0.0, i IN RANGE(0, SIZE(person_A_vector)-1) | sum + person_A_vector[i]^2)) AS A_personMagnitude,
         SQRT(REDUCE(sum = 0.0, i IN RANGE(0, SIZE(person_N_vector)-1) | sum + person_N_vector[i]^2)) AS N_personMagnitude,
         SQRT(REDUCE(sum = 0.0, i IN RANGE(0, SIZE(query_O_vector)-1) | sum + query_O_vector[i]^2)) AS O_queryMagnitude,
         SQRT(REDUCE(sum = 0.0, i IN RANGE(0, SIZE(query_C_vector)-1) | sum + query_C_vector[i]^2)) AS C_queryMagnitude,
         SQRT(REDUCE(sum = 0.0, i IN RANGE(0, SIZE(query_E_vector)-1) | sum + query_E_vector[i]^2)) AS E_queryMagnitude,
         SQRT(REDUCE(sum = 0.0, i IN RANGE(0, SIZE(query_A_vector)-1) | sum + query_A_vector[i]^2)) AS A_queryMagnitude,
         SQRT(REDUCE(sum = 0.0, i IN RANGE(0, SIZE(query_N_vector)-1) | sum + query_N_vector[i]^2)) AS N_queryMagnitude
    WITH p, 
         O_dotProduct / (O_personMagnitude * O_queryMagnitude) AS O_similarity,
         C_dotProduct / (C_personMagnitude * C_queryMagnitude) AS C_similarity,
         E_dotProduct / (E_personMagnitude * E_queryMagnitude) AS E_similarity,
         A_dotProduct / (A_personMagnitude * A_queryMagnitude) AS A_similarity,
         N_dotProduct / (N_personMagnitude * N_queryMagnitude) AS N_similarity
    RETURN p.fullName AS p_name, 
           O_similarity, C_similarity, E_similarity, A_similarity, N_similarity, 
           id(p) AS pid, p.tags AS tags, p.age as age
    ORDER BY (O_similarity + C_similarity + E_similarity + A_similarity + N_similarity) DESC;
    """

    parameters = {
        "p_O_embed": person_embeds["O_embed"],
        "p_C_embed": person_embeds["C_embed"],
        "p_E_embed": person_embeds["E_embed"],
        "p_A_embed": person_embeds["A_embed"],
        "p_N_embed": person_embeds["N_embed"]
    }

    driver = init_driver()

    with driver.session() as session:
        result = session.run(query, parameters)
        
        # Initialize a list to collect potential friends
        potential_friends = []

        for record in result:
            potential_friends.append({
                "name": record["p_name"],
                "O_similarity": record["O_similarity"],
                "C_similarity": record["C_similarity"],
                "E_similarity": record["E_similarity"],
                "A_similarity": record["A_similarity"],
                "N_similarity": record["N_similarity"],
                "pid": record["pid"],
                "tags": record["tags"],
                "age": record["age"]
            })

        return potential_friends if potential_friends else None
