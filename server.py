#!flask/bin/python
import os
from flask import Flask, jsonify, request

import psycopg2
import urlparse
import database

try:
    from flask.ext.cors import cross_origin
except:
    from flask_cors import cross_origin

app = Flask(__name__)




# flask url decorators
@app.route('/api/v1/<beer_id>', methods = ['GET'])
@cross_origin()
def respond(beer_id):
    # recommends a similar beer from a get request
    return jsonify(database.get_next_recommendation(beer_id))

if __name__ == '__main__':
    app.run(debug = True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
