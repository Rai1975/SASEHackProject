from neo4j import GraphDatabase

def init_driver():
    uri = "NEO4J_URI"  
    username = "NEO4J_USER"         
    password = "NEO4J_PASSWORD"  
    return GraphDatabase.driver(uri, auth=(username, password))


def run_query(driver, query, parameters):
    with driver.session() as session:
        result = session.run(query, parameters)
        records = [record.data() for record in result]
    return records  