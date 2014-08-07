#!flask/bin/python
import os
from flask import Flask, jsonify, request, make_response
import database



try:
    from flask.ext.cors import cross_origin
except ImportError:
    from flask_cors import cross_origin

app = Flask(__name__)

# flask url decorators

@app.route('/api/v2/user', methods=['POST'])
def new_user():
        print request.headers
        response = make_response(jsonify(database.create_new_user()))
        response.headers['Access-Control-Allow-Origin'] = "*"
        response.headers['Access-Control-Allow-Headers'] = "PRIVATE-TOKEN"
        return response
        # return jsonify(database.create_new_user())

@app.route('/api/v1/<beer_id>', methods = ['GET'])
def respond(beer_id):
    print request.headers
    response = make_response(jsonify(database.get_next_recommendation(beer_id)))
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "PRIVATE-TOKEN"
    return response
    # return jsonify(database.get_next_recommendation(beer_id))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug = True)
