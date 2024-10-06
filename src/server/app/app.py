import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from flask import Flask
from flask_cors import CORS
from classes.person import Person
from neo4j_db.CRUD import create_user 
from neo4j_db.answers import people_names, random_ages, interests_combinations, openness_answers, conscientiousness_answers, neuroticism_answers, agreeableness_answers, extraversion_answers
from API.generate_embeds import get_ocean_embeds, pre_processor

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route(['GET'], "/userData")
def getUserData(id: int):
    pass

def generate_seed_data():
    for i in range(20):
        temp_person = Person(name=people_names[i], 
                            age=random_ages[i], 
                            tags=interests_combinations[i], 
                            )
        temp_person.openness_answers[i]
        temp_person.add_prompt_response(openness_answers[i])
        temp_person.add_prompt_response(conscientiousness_answers[i])
        temp_person.add_prompt_response(extraversion_answers[i])
        temp_person.add_prompt_response(agreeableness_answers[i])
        temp_person.add_prompt_response(neuroticism_answers[i])
        text = pre_processor(temp_person.prompt_responses)
        embeds = get_ocean_embeds(text)
        temp_person.O_embed = embeds[0]
        temp_person.C_embed = embeds[1]
        temp_person.E_embed = embeds[2]
        temp_person.A_embed = embeds[3]
        temp_person.N_embed = embeds[4]
        create_user(temp_person)

if __name__ == '__main__':
    generate_seed_data()
    # app.run(debug=True)