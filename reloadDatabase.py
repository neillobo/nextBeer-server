"""
script for resetting the database whenever new data files are uploaded
"""


import urlparse
import psycopg2
import os
urlparse.uses_netloc.append("postgres")
# url = urlparse.urlparse(os.environ["DATABASE_URL"])
url = urlparse.urlparse('postgres://postgres@127.0.0.1:5432/beers')

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
print conn

cur = conn.cursor()

try:
    cur.execute("DROP TABLE beers")
except psycopg2.ProgrammingError:
    pass
conn.commit()
cur.execute("CREATE TABLE beer_names(beer_id int PRIMARY KEY NOT NULL, beer_name varchar)")
with open ("./data/beernames100.csv","r") as df:
    values = [tuple(line.strip().split(',')) for line in df]
    cur.executemany("INSERT INTO beer_names VALUES(%s,%s)", values)

try:
    cur.execute("DROP TABLE distances")
except psycopg2.ProgrammingError:
    pass

conn.commit()
cur.execute("CREATE TABLE distances(beer1_id int,beer2_id int, review_overall real, review_aroma real ,review_palate real,review_taste real)")
with open ("./data/distances100.csv","r") as df:
    values = [tuple(line.strip().split(',')) for line in df]
    cur.executemany("INSERT INTO distances VALUES(%s,%s,%s,%s,%s,%s)", values)


conn.commit()
conn.close()
