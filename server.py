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

# API v3 uses the Weighted Slope One Algorithm
@app.route('/api/v3/rate', methods = ['POST'])
def get_best_recommendation():
    unique_string = request.headers['Authorization']
    data = request.json
    beer_id = data['beer_id']
    beer_rating = data['beer_rating']

    user_id = database.get_userid_from_string(unique_string)
    database.save_to_profile(user_id, beer_id, beer_rating)

    recommended_beer_id = database.get_best_recommendation(user_id)
    database.save_recommendation(user_id,recommended_beer_id) # save the recommendation so we dont return it again
    print recommended_beer_id
    return jsonify(database.get_metadata(recommended_beer_id))


@app.route('/api/v2/rate', methods = ['POST'])
def get_next_recommendation():
    '''
    The client sends a POST requests that represents a review of a beer we
    recommended previously. We save this rating and send back a new
    recommendation

    The client identifies itself with its unique_string which it passes
    in the request header
    '''
    unique_string = request.headers['Authorization']
    user_id = database.get_userid_from_string(unique_string)

    if user_id:
        data = request.json
        beer_id = data['beer_id']
        beer_rating = data['beer_rating']

        database.save_to_profile(user_id, beer_id, beer_rating)

        recommended_beer_id = database.get_next_recommendation(user_id)
        # note that this beer has been recommended already
        database.save_to_profile(user_id, recommended_beer_id, 0)

        return jsonify(database.get_metadata(recommended_beer_id))
    else:
        print 'bad unique_string %s' % unique_string
        return jsonify({})

@app.route('/api/v1/<beer_id>', methods = ['GET'])
def get_similar_beer(beer_id):
    '''
    The client sends a get request which represents a request for beers similar
    to the beer in the url
    '''
    recommended_beer_id = database.get_nearest_beer(beer_id)
    if recommended_beer_id:
        return jsonify(database.get_metadata(recommended_beer_id))
    else:
        return jsonify({}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug = True)
