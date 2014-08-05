#!flask/bin/python
import os
from flask import Flask, jsonify, request
import sqlite3
import psycopg2
import urlparse

try:
    from flask.ext.cors import cross_origin
except:
    from flask_cors import cross_origin

app = Flask(__name__)



# utility functions
# these could live in a separate file and be imported here
def run_query(query_string, data):
    """
    describe why this function exists
    what it does should be self-explanatory
    """
    db_connection = sqlite3.connect('beer_distances.db')
    c = db_connection.cursor()
    result = list(c.execute(query_string, (data,)))
    db_connection.close()
    return result

def get_nearest_beers(beer_id, num=10):
    """
    describe why this function exists
    what it does should be self-explanatory
    """
    beers = run_query('SELECT * FROM distances WHERE beer1_id=?', beer_id)
    beers.sort(key=lambda x: x[2])

    if not beers:
        print 'ERROR: no beers found for id', beer_id
    return beers[:num]

def get_metadata(beer_id):
    """
    describe why this function exists
    what it does should be self-explanatory
    """
    name = run_query('SELECT beername FROM beernames WHERE beer_id=?', beer_id)

    metadata = {'name': name[0][0], 'id': beer_id} # leaving room for description, image etc.
    return metadata

def get_next_recommendation(beer_id):
    """
    describe why this function exists
    what it does should be self-explanatory
    """
    top_beers = get_nearest_beers(beer_id)
    if top_beers:
        top_beer = top_beers[0]
        recommended_beer_id = top_beer[1]
        return get_metadata(recommended_beer_id)
    else:
        return {}




def add_to_profile(user_id, beer_id, beer_rating):
    pass

# flask url decorators
@app.route('/api/v1/<beer_id>', methods = ['GET'])
@cross_origin()
def respond(beer_id):
    # recommends a similar beer from a get request
    return jsonify(get_next_recommendation(beer_id))

if __name__ == '__main__':
    app.run(debug = True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
