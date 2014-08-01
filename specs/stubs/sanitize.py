import pandas as pd
import numpy as np
import pylab as pl


def reformat_to_csv():
  with open ('beeradvocate.txt', 'r') as infile:
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
    with open('beer-reviews.csv', 'a') as outfile:
      outfile.write(new_review + '\n')

reformat_to_csv()


# def list_common_reviewers(beer1, beer2)
#   beer_1_reviewers = df[df.beer_name==beer1].review_profilename.unique()
#   beer_2_reviewers = df[df.beer_name==beer2].review_profilename.unique()
#   common_reviewers = set(beer_1_reviewers).intersection(beer_2_reviewers)
#   print "Users in the sameset: %d" % len(common_reviewers)
#   list(common_reviewers)[:10]

# beer1 = "Dale's Pale Ale"
# beer2 = "Fat Tire Amber Ale"
# list_common_reviewers(beer1, beer2)


