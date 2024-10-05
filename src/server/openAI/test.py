import openai
from ..neo4j_db.graph import get_person_tags

openai.api_key=""


print(get_person_tags(1))
