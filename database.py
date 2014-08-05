import sqlite3
import urlparse
import psycopg2
import os

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

db_connection = psycopg2.connect(
   database=url.path[1:],
   user=url.username,
   password=url.password,
   host=url.hostname,
   port=url.port
)
c = db_connection.cursor()

# utility functions
# these could live in a separate file and be imported here
def add_to_profile(user_id, beer_id, beer_rating):
    pass

def run_query(query_string, data):
    """
    describe why this function exists
    what it does should be self-explanatory
    """
    # db_connection = psycopg2.connect("dbname='testdb' user='craig' host='localhost' password='helloworld'")
    c.execute(query_string, (data,))
    result = list(c.fetchall())
    # db_connection.close()
    return result

def get_nearest_beers(beer_id, num=10):
    """
    describe why this function exists
    what it does should be self-explanatory
    """
    beers = run_query('SELECT * FROM distances WHERE beer1_id=%s', beer_id)
    beers.sort(key=lambda x: x[2])

    if not beers:
        print 'ERROR: no beers found for id', beer_id
    return beers[:num]

def get_metadata(beer_id):
    """
    describe why this function exists
    what it does should be self-explanatory
    """
    name = run_query('SELECT beer_name FROM beer_names WHERE beer_id=%s', beer_id)

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