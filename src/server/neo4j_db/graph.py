from neo4j import GraphDatabase

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