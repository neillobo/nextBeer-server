import os
import urlparse
from postgres import Postgres


db_location = os.environ.get('DATABASE_URL', 'postgres://postgres@127.0.0.1:5432/nextbeer')
db = Postgres(db_location)


def get_next_recommendation(user_id):
    return db.one('SELECT beer2_id, sum((m.deviation+u.beer_rating)*m.cardinality)/sum(m.cardinality) AS score FROM \
        reduced_matrix m, reviews u WHERE  m.beer1_id=u.beer_id AND u.user_id=%(user_id)s AND beer2_id IN \
        (SELECT beer2_id FROM reduced_matrix WHERE beer1_id IN (SELECT beer_id FROM reviews where user_id=%(user_id)s))\
         AND beer2_id NOT IN (SELECT beer_id from recommended_beers r where r.user_id=%(user_id)s and r.beer_id is NOT NULL)\
          GROUP BY beer2_id order by score desc limit 1', {'user_id' : user_id})

def save_new_user(unique_string):
    db.run('INSERT INTO users (cookie) VALUES(%(cookie)s)', { 'cookie' : unique_string })

def get_userid_from_string(user_string):
    return db.one('SELECT id FROM users WHERE cookie=%(cookie)s', {'cookie': user_string})

def save_to_profile(user_id, beer_id, beer_rating):
    values = {
        'user_id': user_id,
        'beer_id': beer_id,
        'beer_rating': beer_rating
    }
    db.run('INSERT INTO reviews VALUES (%(user_id)s, %(beer_id)s, %(beer_rating)s)', values)

def save_recommendation(user_id,recommended_beer_id):
    values = {
        'user_id' : user_id,
        'beer_id' : recommended_beer_id
    }
    db.run('INSERT into recommended_beers values(%(user_id)s, %(beer_id)s)', values)

def get_metadata(beer_id):
    metadata = db.one('SELECT beer_id, beer_name, beer_image_url, beer_style, \
        brewery_name, beer_abv FROM beer_names WHERE beer_id=%(beer_id)s', {'beer_id': beer_id})

    return {
        'beer_id': metadata.beer_id,
        'beer_name': metadata.beer_name,
        'beer_image_url': metadata.beer_image_url,
        'beer_style': metadata.beer_style,
        'brewery_name': metadata.brewery_name,
        'beer_abv': metadata.beer_abv
    }

def get_nearest_beer(beer_id):
    try:
        return get_nearest_beers(beer_id, num=1)[0]
    except IndexError:
        return None

def get_nearest_beers(beer_id, num=10):
    return db.all('SELECT beer2_id FROM distances WHERE beer1_id=%(beer_id)s \
        ORDER BY review_overall DESC LIMIT %(num)s', {'beer_id': beer_id, 'num': num})
