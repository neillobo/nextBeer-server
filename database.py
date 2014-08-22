import os
import urlparse
from postgres import Postgres

import string
import random


db_location = os.environ.get("DATABASE_URL", "postgres://postgres@127.0.0.1:5432/postgres")
db = Postgres(db_location)


def get_best_recommendation(user_id):
    recommended_beers =  get_best_recommendations(user_id)
    # print "Recommended beers are ", recommended_beers
    for beerid,distance in recommended_beers:
        is_beer_present = db.one("SELECT beer_id FROM recommended_beers where user_id=%(user_id)s and beer_id=%(beerid)s",{"user_id" : user_id, "beerid":beerid})
        if not is_beer_present:
            return beerid

def get_best_recommendations(user_id):
    return db.all("SELECT beer2_id, sum((m.deviation+u.beer_rating)*m.cardinality)/sum(m.cardinality) AS score FROM \
        reduced_matrix m, reviews u WHERE  m.beer1_id=u.beer_id AND u.user_id=%(user_id)s AND beer2_id IN \
        (SELECT beer2_id FROM reduced_matrix WHERE beer1_id IN (SELECT beer_id FROM reviews where user_id=%(user_id)s))\
         GROUP BY beer2_id order by score desc limit 60",{"user_id" : user_id})

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

def save_recommendation(user_id,recommended_beer_id):
    values = {
        "user_id" : user_id,
        "beer_id" : recommended_beer_id
    }
    db.run("INSERT into recommended_beers values(%(user_id)s, %(beer_id)s)", values)

def get_metadata(beer_id):
    metadata = db.one('SELECT beer_id, beer_name, beer_image_url, beer_style, \
        brewery_name, beer_abv FROM beer_names WHERE beer_id=%(beer_id)s', {"beer_id": beer_id})

    return {
        "beer_id": metadata.beer_id,
        "beer_name": metadata.beer_name,
        "beer_image_url": metadata.beer_image_url,
        "beer_style": metadata.beer_style,
        "brewery_name": metadata.brewery_name,
        "beer_abv": metadata.beer_abv
    }

def get_nearest_beer(beer_id):
    try:
        return get_nearest_beers(beer_id, num=1)[0]
    except IndexError:
        return None


def get_nearest_beers(beer_id, num=10):
    return db.all('SELECT beer2_id FROM distances WHERE beer1_id=%(beer_id)s \
        ORDER BY review_overall DESC LIMIT %(num)s', {"beer_id": beer_id, 'num': num})

def get_next_recommendation(user_id):
    return get_next_recommendations(user_id, 1)[0]

def get_next_recommendations(user_id, num=10):
    '''
    get all beers I like.
    get all users that like a beer I like
    get all the beers they like, count the occurences of each
    return (num) most occuring ones that I haven't rated yet
    '''
    return db.all("SELECT beer_id FROM reviews WHERE beer_rating=1 AND user_id IN \
        (SELECT DISTINCT user_id FROM reviews WHERE beer_rating=1 AND beer_id IN \
            (SELECT DISTINCT beer_id FROM reviews WHERE user_id=%(user_id)s)) \
        AND beer_id NOT IN (SELECT beer_id FROM reviews WHERE user_id=%(user_id)s) \
        GROUP BY beer_id ORDER BY COUNT(*) DESC LIMIT %(num)s", {"user_id": user_id, "num": num})

