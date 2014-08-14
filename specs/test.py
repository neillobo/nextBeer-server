# loading depedencies
import unittest, sys, os

# list of nose.tools can be found at https://nose.readthedocs.org/en/latest/testing_tools.html
from nose.tools import eq_, raises, timed, with_setup

# in order to access objects in database.py
sys.path.insert(0, os.getcwd())

import database
import server

class Test_Unit(object):
    @classmethod
    def setup_class(klass):
        # any setup to run before the class gets instantiated
        pass

    def test_get_nearest_beers(self):
        associated_beer_list = database.get_nearest_beers(2093)
        eq_(len(associated_beer_list), 10, 'get_nearest_beers should return a list of 10 items by default')
        eq_(type(associated_beer_list) is list, True, 'get_nearest_beers should return a list')


    def test_get_metadata(self):
        test_beer_id = 2093
        beer_meta_data = database.get_metadata(test_beer_id)
        eq_(type(beer_meta_data) is dict, True, 'get_meta_data should return a dictionary of metadata about a beer')

        eq_('beer_name' in beer_meta_data, True, 'get_meta_data should return a dictionary with a beer_name property in it')
        eq_(isinstance(beer_meta_data['beer_name'], basestring), True, 'the parameter for beer_name in metadata should be a string')
        eq_(beer_meta_data['beer_name'], '90 Minute IPA', 'the parameter for beer_name in metadata should be "90 Minute IPA"')


        eq_('beer_id' in beer_meta_data, True, 'get_meta_data should return a dictionary with an beer_id in it')
        eq_(isinstance(beer_meta_data['beer_id'], (int, long)), True, 'the parameter for beer_id in metadata should be an int')
        eq_(beer_meta_data['beer_id'], test_beer_id, 'the parameter for name in metadata should be %s' % test_beer_id)

        eq_('beer_image_url' in beer_meta_data, True, 'get_meta_data should return a dictionary with an beer_image_url property in it')
        eq_(isinstance(beer_meta_data['beer_image_url'], basestring), True, 'the parameter for beer_image_url in metadata should be a string')
        eq_(beer_meta_data['beer_image_url'], 'http://cdn.beeradvocate.com/im/beers/2093.jpg', 'the parameter for beer_image_url in metadata should be a http://cdn.beeradvocate.com/im/beers/2093.jpg')

    # def test_get_next_recommendation(self):
    #     beer_recomendation = database.get_next_recommendation(10)
    #     eq_(isinstance(beer_recomendation, (int, long)), True, 'get_next_recommendation should return the id of a beer')
