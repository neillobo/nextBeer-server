import os
import urlparse
from postgres import Postgres

import string
import random


db_location = os.environ.get("DATABASE_URL", "postgres://postgres@127.0.0.1:5432/postgres")
db = Postgres(db_location)


def save_new_user(unique_string):
    db.run("INSERT INTO users (cookie) VALUES(%(cookie)s)", { "cookie" : unique_string })

def get_userid_from_string(user_string):
    return db.one("SELECT id FROM users WHERE cookie=%(cookie)s", {"cookie": user_string})

def save_to_profile(user_id, beer_id, beer_rating):
    values = {
        "user_id": user_id,
        "beer_id": beer_id,
        "beer_rating": beer_rating
    }
    db.run("INSERT INTO reviews VALUES (%(user_id)s, %(beer_id)s, %(beer_rating)s)", values)


def get_metadata(beer_id):
    metadata = db.one('SELECT beer_id, beer_name, beer_image_url  \
        FROM beer_names WHERE beer_id=%(beer_id)s', {"beer_id": beer_id})

    return {
        "beer_id": metadata.beer_id,
        "beer_name": metadata.beer_name,
        "beer_image_url": metadata.beer_image_url
    }

def get_nearest_beers(beer_id, num=10):
    beers = db.all('SELECT * FROM distances WHERE beer1_id=%(beer_id)s \
        OR beer2_id=%(beer_id)s', {"beer_id": beer_id})
    beers.sort(key=lambda x: x[2])

    if not beers:
        print 'ERROR: no beers found for id', beer_id

    return beers[:num]

def get_next_recommendation(user_id):
    return db.one("SELECT beer_id FROM reviews WHERE user_id IN \
        (SELECT DISTINCT user_id FROM reviews WHERE beer_rating=1 AND beer_id IN \
            (SELECT DISTINCT beer_id FROM reviews WHERE user_id=%(user_id)s)) \
        AND beer_id NOT IN (SELECT beer_id FROM reviews WHERE user_id=%(user_id)s) \
        GROUP BY beer_id ORDER BY COUNT(*) DESC LIMIT 1", {"user_id": user_id})


