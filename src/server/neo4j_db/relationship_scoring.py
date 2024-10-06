import numpy as np
from heapq import heappop, heappush
from graph import init_driver
from CRUD import get_person_embeds, get_person_tags
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


def filter_friends(person: Person, potential_friends):
    person_tags = person.tags
    heap = []  

    for p in potential_friends:
        try:
            import numpy as np
            O = np.array(p.O_embed)
            C = np.array(p.C_embed)
            E = np.array(p.E_embed)
            A = np.array(p.A_embed)
            N = np.array(p.N_embed)
            
            # Calculate the average embedding
            avg_sim_score_vector = (O + C + E + A + N) / 5
        except Exception as e:
            print(f"Error processing embeddings for person ID {p.id}: {e}")
            continue  

        score = generate_relationship_score(avg_sim_score_vector, person_tags, p.tags)

        # Use negative score to simulate a max-heap since heapq is a min-heap
        heappush(heap, (-score, (p.id, p.name, p.age)))

    return_list = []
    num_friends_to_return = min(5, len(heap))  # Ensure we don't pop more than available

    for _ in range(num_friends_to_return):
        # heappop returns a tuple: (-score, (id, name, age))
        _, friend_info = heappop(heap)
        return_list.append(friend_info)

    return return_list
    

# Lord forgive me
def generate_relationship_score(vector_sim_score, tags1, tags2):
    return 0.6*(vector_sim_score) + 0.4*(jaccard_similarity(tags1, tags2))

# Finding Potential friends for the user
def find_potential_friends(person_id):
    p_embeds = get_person_embeds(person_id)["vectorEmbeds"]
    query = """
    WITH $p_embeds AS query_vector
    MATCH (p:Person)
    WITH p, query_vector, p.vectorEmbed AS person_vector
    WITH p, query_vector, 
        REDUCE(sum = 0.0, i IN RANGE(0, SIZE(query_vector)-1) | sum + query_vector[i] * person_vector[i]) AS dotProduct,
        REDUCE(sum = 0.0, i IN RANGE(0, SIZE(person_vector)-1) | sum + person_vector[i]^2) AS personMagSquared,
        REDUCE(sum = 0.0, i IN RANGE(0, SIZE(query_vector)-1) | sum + query_vector[i]^2) AS queryMagSquared
    WITH p, dotProduct, SQRT(personMagSquared) AS personMagnitude, SQRT(queryMagSquared) AS queryMagnitude
    WITH p, dotProduct / (personMagnitude * queryMagnitude) AS similarity
    RETURN p.fullName as p_name, similarity, id(p) as pid, p.tags as tags
    ORDER BY similarity DESC;
    """

    parameters = {
        "p_embeds": p_embeds
    }

    driver = init_driver()

    with driver.session() as session:
        result = session.run(query, parameters)
        
        # Initialize a list to collect potential friends
        potential_friends = []

        for record in result:
            potential_friends.append({
                "name": record["p_name"],
                "similarity": record["similarity"],
                "pid": record["pid"],
                "tags": record["tags"]
            })

        return potential_friends if potential_friends else None


def rank_friends(person_id):
    potential_friends = find_potential_friends(person_id)
    person1_tags = get_person_tags(person_id)
    heapq = {}

    for person in potential_friends:
        score = 0.6 * person["similarity"] + 0.4 * (jaccard_similarity(person1_tags, person["tags"]))
        heappush(heapq, (-score, person["pid"]))

    return [heappop(heapq) for _ in range(5)]   
