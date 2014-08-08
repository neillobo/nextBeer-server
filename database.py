import os
import urlparse
from postgres import Postgres

import string
import random


db_location = os.environ.get("DATABASE_URL", "postgres://postgres@127.0.0.1:5432/postgres")
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

def save_new_user(unique_string):
    #creates a new user in the form of unique_id,unique_string in the user database
    print "in save new user function", unique_string
    db.run("INSERT INTO users (cookie) VALUES(%(cookie)s)", { "cookie" : unique_string })


def get_metadata(beer_id):
    """
    returns the metadata for a beer id
    """
    metadata = db.one('SELECT beer_id, beer_name, beer_image_url  \
        FROM beer_names WHERE beer_id=%(beer_id)s', {"beer_id": beer_id})

    return {
        "beer_id": metadata.beer_id,
        "beer_name": metadata.beer_name,
        "beer_image_url": metadata.beer_image_url
    }


def save_to_profile(user_id, beer_id, beer_rating):
    """
    TODO: save a preference for a user in the database
    """
    pass
