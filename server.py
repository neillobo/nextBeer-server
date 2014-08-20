#!flask/bin/python
import os
from flask import Flask, jsonify, request
from flask.ext.cors import CORS
import string
import random
import database

app = Flask(__name__)

# configure a default header
app.config['CORS_HEADERS'] = ['Content-Type','Authorization']
app.config['CORS_RESOURCES'] = {'/api/*': {'origins': '*'}}
CORS(app)


seed_list = list(string.digits + string.uppercase)
@app.route('/api/v3/user', methods=['POST'])
def create_new_user():
    # generate a "random" (36**10 possibilities) identifier for a user
    unique_string = "".join([random.choice(seed_list) for _ in range(10)])

    database.save_new_user(unique_string)
    return jsonify({"token": unique_string})

@app.route('/api/v3/rate', methods = ['POST'])
def get_best_recommendation():
    unique_string = request.headers['Authorization']
    data = request.json
    beer_id = data['beer_id']
    beer_rating = data['beer_rating']

    user_id = database.get_userid_from_string(unique_string)
    database.save_to_profile(user_id, beer_id, beer_rating)
    
    recommended_beer_id = database.get_best_recommendation(user_id).beer2_id
    print recommended_beer_id
    return jsonify(database.get_metadata(recommended_beer_id))


@app.route('/api/v2/rate', methods = ['POST'])
def get_next_recommendation():
    # we get a POST request from the client in JSON format
    # whose request body contains beer_id and beer_rating
    # unique_string comes in "xvgsfddf" as a string
    unique_string = request.headers['Authorization']
    data = request.json
    beer_id = data['beer_id']
    beer_rating = data['beer_rating']

    user_id = database.get_userid_from_string(unique_string)
    database.save_to_profile(user_id, beer_id, beer_rating)

    recommended_beer_id = database.get_next_recommendation(user_id)
    database.save_to_profile(user_id, beer_id, 0) # save it with no rating
    return jsonify(database.get_metadata(recommended_beer_id))

@app.route('/api/v1/<beer_id>', methods = ['GET'])
def get_similar_beer(beer_id):
    try:
        top_beer = database.get_nearest_beers(beer_id, 1)[0]
        recommended_beer_id = top_beer[1]
        return jsonify(database.get_metadata(recommended_beer_id))
    except IndexError:
        return jsonify({})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug = True)
