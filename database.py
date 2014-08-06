import os
import urlparse
from postgres import Postgres

import string
import random

seed_list = list(string.digits + string.uppercase)

db_location = os.environ.get("DATABASE_URL", "postgres://craig:helloworld@127.0.0.1:5432/testdb")
db = Postgres(db_location)

def get_nearest_beers(beer_id, num=10):
    """
    gets n of the most similar beers to a beer id
    """
    beers = db.all('SELECT * FROM distances WHERE beer1_id=%(beer_id)s \
        OR beer2_id=%(beer_id)s', {"beer_id": beer_id})
    beers.sort(key=lambda x: x[2])

    if not beers:
        print 'ERROR: no beers found for id', beer_id

    return beers[:num]

def create_new_user():
    #creates a new user in the form of unique_id,unique_string in the user database
    unique_string = ""
    for i in range(10):
        unique_string += random.choice(seed_list)
    
    try:
        db.run("CREATE TABLE users (id SERIAL, identifier varchar(11))")
    except:
        pass

    
    values = {
        "identifier" : unique_string
    }
    try:
        db.run("INSERT INTO users (identifier) VALUES(%(identifier)s)", values)
        return unique_string
    except:
        return "could not create user"


def get_metadata(beer_id):
    """
    returns the metadata for a beer id
    """
    metadata = db.one('SELECT beer_id, beer_name, beer_image_url  \
        FROM beer_names WHERE beer_id=%(beer_id)s', {"beer_id": beer_id})

    return {
        "id": metadata.beer_id,
        "name": metadata.beer_name,
        "image_url": metadata.beer_image_url
    }

def get_next_recommendation(beer_id):
    top_beers = get_nearest_beers(beer_id)
    if top_beers:
        top_beer = top_beers[0]
        recommended_beer_id = top_beer[1]
        return get_metadata(recommended_beer_id)
    else:
        return {}

def add_to_profile(user_id, beer_id, beer_rating):
    """
    TODO: save a preference for a user in the database
    """
    pass
