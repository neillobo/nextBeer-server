#!flask/bin/python
import os
from flask import Flask, jsonify, request
import sqlite3

try:
    # this is how you would normally import
    from flask.ext.cors import cross_origin
except:
    # support local usage without installed package
    from flask_cors import cross_origin

app = Flask(__name__)

def get_recommendations(beer_id):
    db_connection = sqlite3.connect('beer_distances.db')
    c = db_connection.cursor()
    beers = [row for row in c.execute('SELECT * FROM distances WHERE beer1_id=?', (beer_id,))]
    if not len(beers): print 'ERROR: no beers found for recomendation', beer_id
    beers = sorted(beers, key=lambda x: x[2])
    results = []
    for beer1_id, beer2_id, dist in beers[:10]: # top 10 beers
        name = c.execute('SELECT beername FROM beernames WHERE beer_id=?', (beer2_id,))
        results.append([name.next()[0], dist])
    print results
    db_connection.close()
    return results


def add_to_profile(user_id, beer_id, beer_rating):
    pass

@app.route('/api/v1/<beer_id>', methods = ['GET'])
@cross_origin()
def respond(beer_id):
    # recommends a similar beer from a get request
    return jsonify( { 'recomendations': get_recommendations(beer_id) } )

if __name__ == '__main__':
    app.run(debug = True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)