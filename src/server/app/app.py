import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from flask import Flask, jsonify
from flask_cors import CORS
from classes.person import Person
from neo4j_db.CRUD import create_user, get_person_information, get_persons_friends, get_person_tags
from neo4j_db.answers import people_names, random_ages, interests_combinations, openness_answers, conscientiousness_answers, neuroticism_answers, agreeableness_answers, extraversion_answers
from API.generate_embeds import get_ocean_embeds, pre_processor
from neo4j_db.relationship_scoring import find_potential_friends, filter_friends

app = Flask(__name__)
CORS(app)

# Friends, temp friends, vector search results

def generate_seed_data():
    for i in range(20):
        temp_person = Person(name=people_names[i], 
                            age=random_ages[i], 
                            tags=interests_combinations[i], 
                            )
        temp_person.add_prompt_response(openness_answers[i])
        temp_person.add_prompt_response(conscientiousness_answers[i])
        temp_person.add_prompt_response(extraversion_answers[i])
        temp_person.add_prompt_response(agreeableness_answers[i])
        temp_person.add_prompt_response(neuroticism_answers[i])
        text = pre_processor(temp_person.prompt_responses[0], temp_person.prompt_responses[1], temp_person.prompt_responses[2], temp_person.prompt_responses[3], temp_person.prompt_responses[4])
        embeds = get_ocean_embeds(text)
        temp_person.O_embed = embeds[0]
        temp_person.C_embed = embeds[1]
        temp_person.E_embed = embeds[2]
        temp_person.A_embed = embeds[3]
        temp_person.N_embed = embeds[4]
        create_user(temp_person)

@app.route("/userData/<int:id>", methods=['GET'])
def get_user_data(id: int):
    record = get_person_information(id)
    if record:
        return jsonify(record), 200  
    else:
        return jsonify({"error": "User not found"}), 404  


@app.route("/getFriends/<int:id>", methods=['GET'])
def get_users_friends(id: int):
    record = get_persons_friends(id, 1)

    if record:
        return jsonify(record), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/getTempFriends/<int:id", methods=['GET'])
def get_users_potential_friends(id: int):
    record = get_persons_friends(id, 2)

    if record:
        return jsonify(record), 200
    else:
        return jsonify({"error": "User not found"}), 404
    
@app.route("/getPotentialFriends/<int:id>", methods=['GET'])
def get_potential_new_relationships(id: int):
    ptags = get_person_tags(id)
    pFriends = find_potential_friends(person_id=id)
    
    record = filter_friends(pFriends, ptags)

    if record:
        return jsonify(record), 200
    else:
        return jsonify({"error": "User not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)