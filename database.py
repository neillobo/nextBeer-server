import os
import urlparse
from postgres import Postgres

db_location = os.environ.get("DATABASE_URL", "postgres://craig:helloworld@127.0.0.1:5432/testdb")
db = Postgres(db_location)


def get_nearest_beers(beer_id, num=10):
    """
    gets n of the most similar beers to a beer id
    """
    beers = db.run('SELECT * FROM distances WHERE beer1_id=%(beer_id)s', {"beer_id": beer_id})
    beers.sort(key=lambda x: x[2])

    if not beers:
        print 'ERROR: no beers found for id', beer_id

    return beers[:num]

def get_metadata(beer_id):
    """
    returns the metadata for a beer id
    """
    name = db.one('SELECT beer_name FROM beer_names WHERE beer_id=%(beer_id)s', {"beer_id": beer_id})

    metadata = {
        'name': name,
        'id': beer_id
        # description, image_url etc.
    }

    return metadata

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
