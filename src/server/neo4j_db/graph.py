from neo4j import GraphDatabase
import random
from heapq import heappush, heappop
from relationship_scoring import jaccard_similarity, cosine_similarity
from functools import lru_cache 
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from personality_embedding import pre_processor
from API.generate_embeds import get_embeds 
from answers import openness_answers, conscientiousness_answers, extraversion_answers, agreeableness_answers, neuroticism_answers, people_names, random_ages, interests_combinations, p1, p1_5, p2

def init_driver():
    uri = "neo4j+s://0c5fc78c.databases.neo4j.io"  
    username = "neo4j"         
    password = "SHurLgy9giavsWJRSvzrWrYUEdzjvaQmZAw40pg-I0M"  
    return GraphDatabase.driver(uri, auth=(username, password))


def run_query(driver, query, parameters):
    with driver.session() as session:
        result = session.run(query, parameters)
        records = [record.data() for record in result]
    return records


def generate_alias():
    # whimsical nouns
    adjectives = [
        'Whimsical', 'Wacky', 'Silly', 'Fuzzy', 'Bouncy',
        'Jolly', 'Quirky', 'Sassy', 'Zany', 'Groovy',
        'Cheerful', 'Giggly', 'Bubbly', 'Sparky', 'Nifty',
        'Snazzy', 'Dandy', 'Zesty', 'Dizzy', 'Cuddly',
        'Curly', 'Frothy', 'Lively', 'Doodle', 'Bouncy'
    ]
    
    # a larger list of whimsical nouns
    nouns = [
        'Wombat', 'Platypus', 'Unicorn', 'Panda', 'Octopus',
        'Kangaroo', 'Giraffe', 'Snail', 'Penguin', 'Koala',
        'Bumblebee', 'Dolphin', 'Llama', 'Narwhal', 'Turtle',
        'Monkey', 'Squirrel', 'Elephant', 'Raccoon', 'Flamingo',
        'Hedgehog', 'Dragonfly', 'Puffin', 'Kookaburra', 'Seahorse'
    ]

    # Randomly select an adjective and a noun to create an alias
    alias = f"{random.choice(adjectives)} {random.choice(nouns)}"
    return alias


def create_user(name, embeds, tags, age):
    alias = generate_alias()
    query = """
    CREATE (p:Person {
        fullName: $name,
        tags: $tags,
        age: $age,
        vectorEmbed: $embeds,
        alias: $alias,
        disconnects: []
    })
    """

    # Parameterized query values
    parameters = {
        "name": name,
        "alias": alias,
        "embeds": embeds,
        "tags": tags,
        "age": age
    }

    driver = init_driver()
    run_query(driver=driver, query=query, parameters=parameters)


def modify_disconnects(person_id, new_disconnects):
    query = """
    MATCH (p:Person)
    WHERE id(p) = $person_id
    SET p.disconnects = $new_disconnects
    """
    
    # Parameterized query values
    parameters = {
        "person_id": person_id,
        "new_disconnects": new_disconnects
    }

    driver = init_driver()
    run_query(driver=driver, query=query, parameters=parameters)

def create_relationship(person_id1, person_id2):
    conf_score = generate_relationship_score(person_id1, person_id2)
    query = """
    MATCH (p1:Person), (p2:Person)
    WHERE id(p1) = $person_id1 AND id(p2) = $person_id2
    CREATE (p1)-[r:CONNECTED_TO {
    confidence_score: $conf_score,
    relationship_start_time: datetime(),
    friendship: false
    }]->(p2)
    """
    
    # Parameterized query values
    parameters = {
        "person_id1": person_id1,
        "person_id2": person_id2,
        "conf_score": conf_score
    }

    driver = init_driver()
    run_query(driver=driver, query=query, parameters=parameters)

# Get methods  
  
@lru_cache(maxsize=2)
def get_person_information(person_id):
    query = """
    MATCH (p:Person)
    WHERE id(p) = $person_id
    RETURN p.fullName as Fname, id(p) as id, p.alias as alias, p.age as age;
    """
    
    parameters = {
        "person_id": person_id
    }

    driver = init_driver()

    with driver.session() as session:
        result = session.run(query, parameters)
        
        record = result.single()

        if record:
            return {
                "fullName": record["Fname"],
                "id" : record["id"],
                "alias": record["alias"],
                "age": record["age"]
            }
        else:
            return None  

@lru_cache(maxsize=2)
def get_person_disconnects(person_id):
    query = """
    MATCH (p:Person)
    WHERE id(p) = $person_id
    RETURN p.disconnects as disconnects;
    """
    
    parameters = {
        "person_id": person_id
    }

    driver = init_driver()

    with driver.session() as session:
        result = session.run(query, parameters)
        
        record = result.single()

        if record:
            return {
                "disconnects": record["disconnects"]
            }
        else:
            return None  

@lru_cache(maxsize=2)
def get_person_embeds(person_id):
    query = """
    MATCH (p:Person)
    WHERE id(p) = $person_id
    RETURN p.vectorEmbed as embed;
    """
    
    parameters = {
        "person_id": person_id
    }

    driver = init_driver()

    with driver.session() as session:
        result = session.run(query, parameters)
        
        record = result.single()

        print(record)

        if record:
            return {
                "vectorEmbeds": record["embed"]
            }
        else:
            return None  
        
@lru_cache(maxsize=2)
def get_person_tags(person_id):
    query = """
    MATCH (p:Person)
    WHERE id(p) = $person_id
    RETURN p.tags as tags;
    """
    
    parameters = {
        "person_id": person_id
    }

    driver = init_driver()

    with driver.session() as session:
        result = session.run(query, parameters)
        
        record = result.single()

        if record:
            return {
                "tags": record["tags"]
            }
        else:
            return None 
        

# Lord forgive me
def generate_relationship_score(person_id1, person_id2):
    personality_p1 = get_person_embeds(person_id1)["vectorEmbeds"]
    personality_p2 = get_person_embeds(person_id2)["vectorEmbeds"]

    # Computing similarity in personality
    personality_similarity = cosine_similarity(personality_p1, personality_p2)

    p1_tags = get_person_tags(person_id1)
    p2_tags = get_person_tags(person_id2)

    # Computing similarity in tags
    tags_similarity = jaccard_similarity(p1_tags, p2_tags)

    # Fetch ages
    age_p1 = get_person_information(person_id1)["age"]
    age_p2 = get_person_information(person_id2)["age"]

    # Calculate age difference
    age_difference = abs(age_p1 - age_p2)

    # Normalize age similarity
    # Define a maximum acceptable age difference for full score
    max_age_difference = 20  # You can adjust this based on your requirements
    if age_difference <= max_age_difference:
        age_similarity = 1 - (age_difference / max_age_difference)  # Score ranges from 0 to 1
    else:
        age_similarity = 0  # If the difference is greater than max, score is 0

    # Combine scores with appropriate weights
    final_score = (0.5 * personality_similarity) + (0.4 * tags_similarity) + (0.1 * age_similarity)

    return final_score

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



for i in range(20):
    name = people_names[i]
    text = pre_processor(openness_answers[i], 
                        conscientiousness_answers[i], 
                        extraversion_answers[i], 
                        agreeableness_answers[i], 
                        neuroticism_answers[i])
    
    embeds = get_embeds(text)
    age = random_ages[i]
    tags = interests_combinations[i]
    
    create_user(name=name, embeds=embeds, tags=tags, age=age)

# print(find_potential_friends(14))



def rank_friends(person_id):
    potential_friends = find_potential_friends(person_id)
    person1_tags = get_person_tags(person_id)
    heapq = {}

    for person in potential_friends:
        score = 0.6 * person["similarity"] + 0.4 * (jaccard_similarity(person1_tags, person["tags"]))
        heappush(heapq, (-score, person["pid"]))

    return [heappop(heapq) for _ in range(5)]   