import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from neo4j_db.graph import init_driver, run_query
import random
from classes.person import Person
from functools import lru_cache 

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


def create_user(p1: Person, hashed_password, email):
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
        O_embed: $O_embed,
        C_embed: $C_embed,
        E_embed: $E_embed,
        A_embed: $A_embed,
        N_embed: $N_embed,
        alias: $alias,
        email: $email,
        password: $hashed_password,
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
        "age": age,
        "email": email,
        "hashed_password": hashed_password
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

def create_potential_match(person1_id, person2_id):
    query = """
    MATCH (p1:Person), (p2:Person)
    WHERE id(p1) = $person_id1 AND id(p2) = $person_id2
    CREATE (p1)-[r:CONNECTED_TO {
    relationship_start_time: datetime(),
    friendship: false
    }]->(p2)
    """
    
    # Parameterized query values
    parameters = {
        "person_id1": person1_id,
        "person_id2": person2_id,
    }

    driver = init_driver()
    run_query(driver=driver, query=query, parameters=parameters)


def create_friendship_req(p1_id, p2_id):
    query = """
    MATCH (p1:Person), (p2: Person)
    WHERE id(p1) = $p1_id AND id(p2) = $p2_id
    CREATE (p1)-[:FRIEND_REQUEST {sent_at: datetime()}]->(p2)
    RETURN p1, p2
    """
    parameters={
        "p1_id": p1_id,
        "p2_id": p2_id
    }

    driver = init_driver()
    run_query(driver, query, parameters)

def validate_friend_req(p1_id, p2_id):
    query1 = """
    MATCH (p1:Person)-[r:FRIEND_REQUEST]->(p2:Person)
    WHERE id(p1) = $p1_id AND id(p2) = $p2_id
    RETURN COUNT(*) as count1
    """
    
    query2 = """
    MATCH (p2:Person)-[r:FRIEND_REQUEST]->(p1:Person)
    WHERE id(p1) = $p1_id AND id(p2) = $p2_id
    RETURN COUNT(*) as count2
    """

    create_connection_query = """
    MATCH (p1:Person), (p2:Person)
    WHERE id(p1) = $p1_id AND id(p2) = $p2_id
    CREATE (p1)-[:CONNECTED_TO {friendship: true, connected_at: datetime()}]->(p2),
           (p2)-[:CONNECTED_TO {friendship: true, connected_at: datetime()}]->(p1)
    """

    delete_friend_request_query = """
    MATCH (p1:Person)-[r1:FRIEND_REQUEST]->(p2:Person),
          (p2:Person)-[r2:FRIEND_REQUEST]->(p1:Person)
    WHERE id(p1) = $p1_id AND id(p2) = $p2_id
    DELETE r1, r2
    """

    parameters = {
        "p1_id": p1_id,
        "p2_id": p2_id
    }

    driver = init_driver()

    with driver.session() as session:
        # Check if friend requests exist both ways
        result1 = session.run(query1, parameters)
        result2 = session.run(query2, parameters)

        record1 = result1.single()
        record2 = result2.single()

        if record1["count1"] > 0 and record2["count2"] > 0:
            # If friend requests exist both ways, create the CONNECTED_TO relationships
            session.run(create_connection_query, parameters)
            # Then delete the FRIEND_REQUEST relationships
            session.run(delete_friend_request_query, parameters)
            return "Friendship established!"
        else:
            return "Friend request not mutual or not found."
  

def delete_old_relationships():
    query = """
    MATCH (p1)-[r:CONNECTED_TO]->(p2)
    WHERE r.friendship = false 
    AND r.relationship_start_time < datetime() - duration({ hours: 48 })
    WITH p1, p2, r
    SET p1.disconnects = COALESCE(p1.disconnects, []) + [id(p2)],
        p2.disconnects = COALESCE(p2.disconnects, []) + [id(p1)]
    DELETE r
    """
    
    driver = init_driver()
    run_query(driver=driver, query=query)

def delete_existing_relationship(p1_id, p2_id):
    query="""
    MATCH (p1:Person)-[r:CONNECTED_TO]->(p2:Person)
    WHERE id(p1) = $p1_id AND id(p2) = $p2_id
    DELETE r
    WITH p1, p2
    SET p1.disconnected = coalesce(p1.disconnected, []) + [p2.id],
        p2.disconnected = coalesce(p2.disconnected, []) + [p1.id]
    RETURN p1, p2
    """
    parameters={
        "p1_id": p1_id,
        "p2_id": p2_id
    }

    driver = init_driver()
    run_query(driver, query, parameters)

# Get methods  
@lru_cache(maxsize=2)
def get_person_information(email):
    query = """
    MATCH (p:Person)
    WHERE p.email = $email
    RETURN p.fullName as Fname, id(p) as id, p.alias as alias, p.age as age, p.tags as tags;
    """
    
    parameters = {
        "email": email
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
                "age": record["age"],
                "tags": record["tags"]
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
    RETURN p.O_embed AS O_embed, p.C_embed AS C_embed, p.E_embed AS E_embed, p.A_embed AS A_embed, p.N_embed AS N_embed;
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
                "O_embed": record["O_embed"],
                "C_embed": record["C_embed"],
                "E_embed": record["E_embed"],
                "A_embed": record["A_embed"],
                "N_embed": record["N_embed"]
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

@lru_cache(maxsize=2)
def get_persons_friends(person_id, flag):
    query1 = """
    MATCH (p1:Person)-[r:CONNECTED_TO]-(p2:Person)
    WHERE id(p1) = $person_id 
    AND r.friendship = true
    RETURN p2.id as id, p2.fullName as name, p2.tags as tags, p2.age as age 
    """ 

    query2 = """
    MATCH (p1:Person)-[r:CONNECTED_TO]-(p2:Person)
    WHERE id(p1) = $person_id 
    AND r.friendship = false
    AND r.relationship_start_time < datetime() - duration({ hours: 48 })
    RETURN p2.id as id, p2.fullName as name, p2.tags as tags, p2.age as age 
    """    
    parameters = {
        "person_id": person_id
    }

    driver = init_driver()

    query = query1 if flag == 1 else query2

    with driver.session() as session:
        result = session.run(query, parameters)

        friends = []

        for record in result:
            friends.append({
                "name": record["name"],
                "id": record["id"],
                "tags": record["tags"],
                "age": record["age"]
            }) 

        if friends:
            return friends
        else:
            return None