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

@app.route('/api/v3/user', methods=['POST'])
@app.route('/api/v2/user', methods=['POST'])
def create_new_user():
    '''
    Generate a random (36**10 possibilities) identifier for the client
    This request is made when the app starts the very first time.
    The client then uses this unique_string as an identifier in all subsequent
    requests it makes.
    The unique_string can be thought of as a randomly generated username.
    '''
    possible_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ' # string.digits + string.uppercase
    unique_string = ''.join([random.choice(possible_chars) for _ in range(10)])

    database.save_new_user(unique_string)
    return jsonify({"token": unique_string})

# API v3 uses the Weighted Slope One Algorithm
@app.route('/api/v3/rate', methods = ['POST'])
def get_best_recommendation():
    '''
    The client sends a POST requests that represents a review of a beer we
    recommended previously. We save this rating and send back a new
    recommendation

    The client identifies itself with its unique_string which it passes
    in the request header
    '''
    try:
        unique_string = request.headers['Authorization']
    except KeyError:
        print 'client sent review without auth'
        return jsonify({}), 401

    user_id = database.get_userid_from_string(unique_string)
    if not user_id:
        print 'bad unique_string %s' % unique_string
        return jsonify({}), 401

    review = request.json
    if not review:
        print 'did not get a json review'
        return jsonify({}), 400

    try:
        beer_id = review['beer_id']
        beer_rating = review['beer_rating']
    except KeyError as missing_param:
        print 'Review missing parameter %s' % missing_param
        return jsonify({}), 400
    if not isinstance(beer_id, int) or  not isinstance(beer_rating, int):
        print 'The client shuld be passing review parameters as integers. Possibly SQL injection.'
        print beer_id, beer_rating
        return jsonify({}), 400

    database.save_to_profile(user_id, beer_id, beer_rating)

    recommended_beer_id = database.get_next_recommendation(user_id)
    database.save_recommendation(user_id,recommended_beer_id) # save the recommendation so we dont return it again
    return jsonify(database.get_metadata(recommended_beer_id))


@app.route('/api/v1/<beer_id>', methods = ['GET'])
def get_similar_beer(beer_id):
    '''
    The client sends a get request which represents a request for beers similar
    to the beer in the url
    '''
    try:
        beer_id = int(beer_id)
    except ValueError as e:
        print 'Bad beer id %s' % beer_id
        return jsonify({}), 400

    recommended_beer_id = database.get_nearest_beer(beer_id)
    if recommended_beer_id:
        return jsonify(database.get_metadata(recommended_beer_id))
    else:
        return jsonify({}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug = True)
