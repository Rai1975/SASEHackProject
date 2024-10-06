import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import random
from graph import init_driver, run_query
from functools import lru_cache 
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from classes.person import Person

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


def create_user(p1: Person):
    alias = generate_alias()
    name = p1.name
    age = p1.age
    tags = p1.tags
    O_embed = p1.O_embed
    C_embed = p1.C_embed
    E_embed = p1.E_embed
    A_embed = p1.A_embed
    N_embed = p1.N_embed
    
    query = """
    CREATE (p:Person {
        fullName: $name,
        tags: $tags,
        age: $age,
        O_embed = p1.O_embed,
        C_embed = p1.C_embed,
        E_embed = p1.E_embed,
        A_embed = p1.A_embed,
        N_embed = p1.N_embed,
        alias: $alias,
        disconnects: []
    })
    """

    # Parameterized query values
    parameters = {
        "name": name,
        "alias": alias,
        "O_embed": O_embed,
        "C_embed": C_embed,
        "E_embed": E_embed,
        "A_embed": A_embed,
        "N_embed": N_embed,
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

def create_relationship(person1: Person, person2: Person, conf_score):
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
        "person_id1": person1.id,
        "person_id2": person2.id,
        "conf_score": conf_score
    }

    driver = init_driver()
    run_query(driver=driver, query=query, parameters=parameters)

def delete_old_relationships():
    query = """
    MATCH (p1)-[r:CONNECTED_TO]->(p2)
    WHERE r.friendship = false 
    AND r.relationship_start_time < datetime() - duration({ hours: 48 })
    DELETE r
    """
    
    driver = init_driver()
    run_query(driver=driver, query=query)

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
        
