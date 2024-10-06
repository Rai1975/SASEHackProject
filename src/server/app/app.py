import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from flask import Flask, jsonify, request
from flask_cors import CORS
from classes.person import Person
from neo4j_db.CRUD import create_user, get_person_information, get_persons_friends, get_person_tags, create_friendship_req, delete_existing_relationship, validate_friend_req, create_potential_match
from neo4j_db.answers import people_names, random_ages, interests_combinations, openness_answers, conscientiousness_answers, neuroticism_answers, agreeableness_answers, extraversion_answers
from neo4j_db.benchmark import get_embeds_fine
from neo4j_db.relationship_scoring import find_potential_friends, filter_friends

app = Flask(__name__)
CORS(app)


# def generate_seed_data():
#     for i in range(20):
#         temp_person = Person(name=people_names[i], 
#                             age=random_ages[i], 
#                             tags=interests_combinations[i], 
#                             )
#         temp_person.add_prompt_response(openness_answers[i])
#         temp_person.add_prompt_response(conscientiousness_answers[i])
#         temp_person.add_prompt_response(extraversion_answers[i])
#         temp_person.add_prompt_response(agreeableness_answers[i])
#         temp_person.add_prompt_response(neuroticism_answers[i])
#         prompts = [openness_answers[i], conscientiousness_answers[i], extraversion_answers[i], agreeableness_answers[i], neuroticism_answers[i]]
#         embeds = []
#         for j in prompts:
#             embeds.append(get_embeds_fine(j)[0])
#         temp_person.O_embed = embeds[0]
#         temp_person.C_embed = embeds[1]
#         temp_person.E_embed = embeds[2]
#         temp_person.A_embed = embeds[3]
#         temp_person.N_embed = embeds[4]
#         create_user(temp_person, "33zx-s3d-dd", f"{people_names[i][0:3]}email.com")

@app.route("/api/userData/", methods=['GET'])
def get_user_data(id: int):
    email = request.args.get('email')
    record = get_person_information(id)
    if record:
        return jsonify(record), 200  
    else:
        return jsonify({"error": "User not found"}), 404  


@app.route("/api/getFriends/<int:id>", methods=['GET'])
def get_users_friends(id: int):
    record = get_persons_friends(id, 1)

    if record:
        return jsonify(record), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/api/getTempFriends/<int:id>", methods=['GET'])
def get_users_potential_friends(id: int):
    record = get_persons_friends(id, 2)

    if record:
        return jsonify(record), 200
    else:
        return jsonify({"error": "User not found"}), 404
    
@app.route("/api/getPotentialFriends/<int:id>", methods=['GET'])
def get_potential_new_relationships(id: int):
    ptags = get_person_tags(id)
    pFriends = find_potential_friends(person_id=id)
    
    record = filter_friends(pFriends, ptags)

    if record:
        return jsonify(record), 200
    else:
        return jsonify({"error": "User not found"}), 404
    
@app.route("/api/postCreateUser", methods=['POST'])
def post_user_creation(response):
    try:
        # Extract the JSON package sent by the client
        response = request.get_json()

        # Ensure required fields are present
        if not all(key in response for key in ("name", "tags", "age", "prompt", "hashed_password", "email")):
            return jsonify({"error": "Missing required fields"}), 400

        # Create a new Person object
        p1 = Person(response["name"], response["tags"], response["age"])

        # Add responses to prompts
        for answer in response["prompt"]:
            p1.add_prompt_response(answer)

        # Generate OCEAN embeddings (assuming this is a function that returns the 5 factors)
        # embeds = []
        # for i in p1.prompt_responses:
        #     embeds.append(get_embeds_fine(p1.prompt_responses))
            
        # p1.O_embed = embeds[0]
        # p1.C_embed = embeds[1]
        # p1.E_embed = embeds[2]
        # p1.A_embed = embeds[3]
        # p1.N_embed = embeds[4]

        # Create the user (assuming create_user is a function to handle this logic)
        create_user(p1, response["hashed_password"], response["email"])

        # Return a success response
        return jsonify({"message": "User created successfully"}), 201

    except Exception as e:
        # Handle any potential errors
        return jsonify({"error": str(e)}), 500

@app.route("/api/sendFriendReq/<int:id1>/<int:id2>", methods=['POST'])
def sendFriendReq(id1, id2):
    create_friendship_req(p1_id=id1, p2_id=id2)
    return jsonify({"message": "Friend request sent"}), 200

@app.route("/api/validateFriendReq/<int:id1>/<int:id2>", methods=['POST'])
def validateFriendReq(id1, id2):
    result = validate_friend_req(id1, id2)
    return jsonify({"message": result}), 200

@app.route("/api/swipeRight/<int:id1>/<int:id2>", methods=['POST'])
def swipeRight(id1, id2):
    create_potential_match(id1, id2)
    return jsonify({"message": "Swiped Right!"}), 200


if __name__ == '__main__':
    # generate_seed_data()
    app.run(debug=True)