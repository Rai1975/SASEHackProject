from neo4j import GraphDatabase

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


def create_user(name, alias, embeds, tags):
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


def get_person_information(person_id):
    query = """
    MATCH (p:Person {id: $person_id})
    RETURN p.fullName as Fname, p.tags as tags, p.alias as alias;
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
                "tags": record["tags"],
                "alias": record["alias"]
            }
        else:
            return None  


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
        