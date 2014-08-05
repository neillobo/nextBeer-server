import sqlite3
# utility functions
# these could live in a separate file and be imported here
def add_to_profile(user_id, beer_id, beer_rating):
    pass

def run_query(query_string, data):
    """
    describe why this function exists
    what it does should be self-explanatory
    """
    db_connection = sqlite3.connect('beer_distances.db')
    c = db_connection.cursor()
    result = list(c.execute(query_string, (data,)))
    db_connection.close()
    return result

def get_nearest_beers(beer_id, num=10):
    """
    describe why this function exists
    what it does should be self-explanatory
    """
    beers = run_query('SELECT * FROM distances WHERE beer1_id=?', beer_id)
    beers.sort(key=lambda x: x[2])

    if not beers:
        print 'ERROR: no beers found for id', beer_id
    return beers[:num]

def get_metadata(beer_id):
    """
    describe why this function exists
    what it does should be self-explanatory
    """
    name = run_query('SELECT beername FROM beernames WHERE beer_id=?', beer_id)

    metadata = {'name': name[0][0], 'id': beer_id} # leaving room for description, image etc.
    return metadata

def get_next_recommendation(beer_id):
    """
    describe why this function exists
    what it does should be self-explanatory
    """
    top_beers = get_nearest_beers(beer_id)
    if top_beers:
        top_beer = top_beers[0]
        recommended_beer_id = top_beer[1]
        return get_metadata(recommended_beer_id)
    else:
        return {}