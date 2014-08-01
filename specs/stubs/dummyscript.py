import pandas as pd
import numpy as np
import pylab as pl

from sklearn.metrics.pairwise import euclidean_distances


def reformat_to_csv():
  with open ('dummy-origin-data.txt', 'r') as infile:
    dataset = infile.read().split('\n\n')
  field_names = ['beer/name', 'beer/beerId', 'beer/brewerId','beer/ABV', 'beer/style', 'review/appearance', 'review/aroma', 'review/palate' ,'review/taste', 'review/overall', 'review/profileName']
  simpler_field_names = ['beer_name', 'beer_id', 'brewer_id', 'abv', 'style', 'review_appearence', 'review_aroma', 'review_palate', 'review_taste', 'review_overall','review_profilename']
  data = []
  data.append(', '.join(field_names))
  for review in dataset:
    lines = review.split('\n')
    entry = []
    for line in lines:
      words = line.split(' ')
      key = words[0][:-1]
      if key in field_names:
        value = ' '.join(words[1:])
        entry.append(value)
    data.append(','.join(entry))
  for new_review in data:
    # print new_review
    with open('dummy-data.csv', 'a') as outfile:
      outfile.write(new_review + '\n')


def read_csv(file_path):
  return pd.read_csv(file_path, error_bad_lines=False)

df = read_csv("./beer_reviews/beer_reviews.csv")

def find_common_reviewers(beer_1, beer_2):
  beer_1_reviewers = df[df.beer_name==beer_1].review_profilename.unique()
  beer_2_reviewers = df[df.beer_name==beer_2].review_profilename.unique()
  common_reviewers = set(beer_1_reviewers).intersection(beer_2_reviewers)
  return common_reviewers


def get_beer_reviews(beer, common_users):
  mask = (df.review_profilename.isin(common_users)) & (df.beer_name == beer)
  reviews = df[mask].sort('review_profilename')
  reviews = reviews[reviews.review_profilename.duplicated() == False]
  return reviews


def calculate_similarity(beer1,beer2):
  dists = []
  ALL_FEATURES = ['review_overall','review_aroma','review_palate','review_taste']
  #function to find the common reviewers
  common_reviewers = find_common_reviewers(beer1,beer2)
  #getting the reviews
  beer_1_reviews = get_beer_reviews(beer1,common_reviewers)
  beer_2_reviews = get_beer_reviews(beer2,common_reviewers)
  for f in ALL_FEATURES:
    dists.append(euclidean_distances(beer_1_reviews[f], beer_2_reviews[f])[0][0])
  return dists


def calc_distance(dists, beer1, beer2, weights):
    mask = (dists.beer1==beer1) & (dists.beer2==beer2)
    row = dists[mask]
    row = row[['overall_dist', 'aroma_dist', 'palate_dist', 'taste_dist']]
    dist = weights * row
    # print "Distance is", dist
    return dist.sum(axis=1).tolist()[0]


def create_data_frame(beer_list):
  cols = ["beer1","beer2","overall_dist","aroma_dist","palate_dist","taste_dist"]
  simple_distances = calculate_similarity_all(beer_list)
  return pd.DataFrame(simple_distances, columns = cols)


def find_similar_beers(beer_name, num_of_results):
  my_beer = beer_name
  results = []
  for b in beers:
      if my_beer!=b:
          results.append((my_beer, b, calc_distance(simple_distances, my_beer, b, weights)))
  # num_of_results shouldn't exceed the number of items to be sorted
  return sorted(results, key=lambda x: x[2])[:num_of_results]
