#!flask/bin/python
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_recommendation(user_id):
    # do we send them the picture
    return {'beer_id': 123, 'beer_name': 'Asdf Beer', 'beer_description': 'it\'s beer man'}

def add_to_profile(user_id, beer_id, beer_rating):
    pass

@app.route('/api/v1/', methods = ['GET'])
def respond():
    print request.headers
    
    # from request
    unique_id = 1234 
    beer_id = 4321
    beer_rating = 1
    
    add_to_profile(unique_id, beer_id, beer_rating)
    return jsonify( { 'recomendation': get_next_recommendation(unique_id) } )

if __name__ == '__main__':
    app.run(debug = True)
