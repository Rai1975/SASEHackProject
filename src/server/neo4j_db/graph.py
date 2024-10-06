from neo4j import GraphDatabase
import random
from heapq import heappush, heappop
from relationship_scoring import jaccard_similarity, cosine_similarity
from functools import lru_cache 
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from classes.person import Person
from personality_embedding import pre_processor
from API.generate_embeds import get_ocean_embeds 
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