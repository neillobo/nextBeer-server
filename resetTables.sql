DROP TABLE beer_names;
DROP TABLE distances;
DROP TABLE users;
DROP TABLE reviews;

CREATE TABLE beer_names(beer_id int PRIMARY KEY NOT NULL, beer_name varchar, beer_image_url varchar, beer_style varchar, brewery_name varchar, beer_abv real);
CREATE TABLE distances(beer1_id int, beer2_id int, review_overall real, review_aroma real ,review_palate real,review_taste real);
CREATE TABLE users (id SERIAL, cookie varchar(11));
CREATE TABLE reviews (user_id int, beer_id int, beer_rating int);

\COPY beer_names FROM './data/metadata.csv' DELIMITER ',' CSV HEADER;
\COPY distances FROM './data/distances.csv' DELIMITER ',' CSV HEADER;
\COPY users FROM './data/usernames.csv' DELIMITER ',' CSV HEADER;
\COPY reviews FROM './data/reviews.csv' DELIMITER ',' CSV HEADER;
