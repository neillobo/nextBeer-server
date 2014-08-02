#!flask/bin/python
import os
from flask import Flask, jsonify, request

try:
    # this is how you would normally import
    from flask.ext.cors import cross_origin
except:
    # support local usage without installed package
    from flask_cors import cross_origin

app = Flask(__name__)

def get_recommendation(user_id):
    # do we send them the picture
    return {'beer_id': 123, 'beer_name': 'Asdf Beer', 'beer_description': 'it\'s beer man'}

def add_to_profile(user_id, beer_id, beer_rating):
    pass

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/api/v1/', methods = ['GET', 'POST'])
@cross_origin(headers=['Content-Type'])
def respond():
    print request.headers

    # from request
    unique_id = 1234
    beer_id = 4321
    beer_rating = 1

    add_to_profile(unique_id, beer_id, beer_rating)
    return jsonify( { 'recomendation': get_recommendation(unique_id) } )

if __name__ == '__main__':
    app.run(debug = True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
