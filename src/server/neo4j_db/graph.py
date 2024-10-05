from neo4j import GraphDatabase
import random
from app.relationship_scoring import generate_relationship_score
from cache import LruCache

def init_driver():
    uri = "neo4j+s://f9abbebf.databases.neo4j.io"  
    username = "neo4j"         
    password = "sF2U5HO-3zyrCrwRRYKkTu9G-TTHZlh4kRL5_HFbRqQ"  
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


def create_user(name, embeds, tags):
    alias = generate_alias()
    query = """
    CREATE (p:Person {
        fullName: $name,
        tags: $tags,
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
        "tags": tags
    }

    driver = init_driver()
    run_query(driver=driver, query=query, parameters=parameters)


def modify_disconnects(person_id, new_disconnects):
    query = """
    MATCH (p:Person {id: $person_id})
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
    MATCH (p1:Person {id: $person_id1 }), (p2:Person {id: $person_id2})
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
  
@LruCache(maxsize=2, timeout=1)
def get_person_information(person_id):
    query = """
    MATCH (p:Person {id: $person_id})
    RETURN p.fullName as Fname, id(p) as id, p.alias as alias;
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
                "alias": record["alias"]
            }
        else:
            return None  

@LruCache(maxsize=2, timeout=1)
def get_person_disconnects(person_id):
    query = """
    MATCH (p:Person {id: $person_id})
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

@LruCache(maxSize=2, timeout=1)
def get_person_embeds(person_id):
    query = """
    MATCH (p:Person {id: $person_id})
    RETURN p.vectorEmbed as embed;
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
                "vectorEmbeds": record["embed"]
            }
        else:
            return None  
        
@LruCache(maxSize=2, timeout=1)
def get_person_tags(person_id):
    query = """
    MATCH (p:Person {id: $person_id})
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