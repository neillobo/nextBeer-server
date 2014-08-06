import sqlite3
import urlparse
import psycopg2
import os

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

print 'database_url', url
print 'port', url.port

db_connection = psycopg2.connect(
   database=url.path[1:],
   user=url.username,
   # password=url.password,
   host=url.hostname,
   port=url.port
)
c = db_connection.cursor()

def run_query(query_string, data):
    """
    abstract away queries for easy switching between databases
    """
    # db_connection = psycopg2.connect("dbname='testdb' user='craig' host='localhost' password='helloworld'")
    c.execute(query_string, (data,))
    result = list(c.fetchall())
    # db_connection.close()
    return result

def get_nearest_beers(beer_id, num=10):
    """
    gets n of the most similar beers to a beer id
    """
    beers = run_query('SELECT * FROM distances WHERE beer1_id=%s', beer_id)
    beers.sort(key=lambda x: x[2])

    if not beers:
        print 'ERROR: no beers found for id', beer_id

    return beers[:num]

def get_metadata(beer_id):
    """
    returns the metadata for a beer id
    """
    name = run_query('SELECT beer_name FROM beer_names WHERE beer_id=%s', beer_id)[0][0]

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
    TODO: save a perefernce for a user in the database
    """
    pass
