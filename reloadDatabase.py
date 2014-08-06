"""
script for resetting the database whenever new data files are uploaded
"""

import urlparse
from postgres import Postgres
import os

distances_file_name  = "./data/distances.csv"
beer_names_file_name = "./data/metadata.csv"

db_location = os.environ.get("DATABASE_URL", "postgres://postgres@127.0.0.1:5432/postgres")
db = Postgres(db_location)

try:
    db.run("DROP TABLE beer_names")
except:
    pass

db.run("CREATE TABLE beer_names(beer_id int PRIMARY KEY NOT NULL, beer_name varchar, beer_image_url varchar)")
with open (beer_names_file_name,"r") as infile:
    for line in infile:
        comma_seperated_values = line.strip().split(',')
        values = {
            "beer_id" : comma_seperated_values[0],
            "beer_name" : comma_seperated_values[1],
            "beer_image_url": comma_seperated_values[2]
        }
        db.run("INSERT INTO beer_names VALUES(%(beer_id)s,%(beer_name)s,%(beer_image_url)s)", values)

try:
    db.run("DROP TABLE distances")
except:
    pass


db.run("CREATE TABLE distances(beer1_id int,beer2_id int, review_overall real, \
    review_aroma real ,review_palate real,review_taste real)")
with open (distances_file_name,"r") as infile:
    for line in infile:
        comma_seperated_values = line.strip().split(',')
        values = {
            "beer1_id": comma_seperated_values[0],
            "beer2_id": comma_seperated_values[1],
            "review_overall": comma_seperated_values[2],
            "review_aroma": comma_seperated_values[3],
            "review_palate": comma_seperated_values[4],
            "review_taste": comma_seperated_values[5]
        }
        db.run("INSERT INTO distances VALUES(%(beer1_id)s, %(beer2_id)s, \
            %(review_overall)s, %(review_aroma)s, %(review_palate)s, %(review_taste)s)", values)

