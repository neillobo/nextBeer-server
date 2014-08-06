# loading depedencies
import unittest, sys, os

# list of nose.tools can be found at https://nose.readthedocs.org/en/latest/testing_tools.html
from nose.tools import eq_, raises, timed, with_setup

# in order to access objects in database.py
sys.path.insert(0, os.getcwd())
import database

class Test_Unit(object):
  """
  This is a test Class. The nose test framework
  prescribes that a test class name should be
  prefixed with Test.
  """


  @classmethod
  def setup_class(klass):
    print "any setup to run before the class gets instantiated"


  def sample_test(self):
    """
    follow the structure of this test to create new, meaningful unit tests in the future
    """
    the_thing_to_test = 'DH'
    # if both args are equal, it passes
    # alternatively you could write
    # assert the_thing_to_test, 'DH'
    eq_(the_thing_to_test, 'DH')

  def test_create_new_user(self):
    new_identifier = database.create_new_user()
    eq_(len(new_identifier), 10, 'create_new_user return should be of length 10')
    eq_(type(new_identifier)) is str, True, 'create_new_user should return a string'

  def test_get_nearest_beers(self):
    associated_beer_list = database.get_nearest_beers(2093)
    eq_(len(associated_beer_list), 10, 'get_nearest_beers should return a list of 10 items by default')
    eq_(type(associated_beer_list) is list, True, 'get_nearest_beers should return a list')


  def test_get_metadata(self):
    test_beer_id = 2093
    beer_meta_data = database.get_metadata(test_beer_id)
    eq_(type(beer_meta_data) is dict, True, 'get_meta_data should return a dictionary of metadata about a beer')

    eq_('name' in beer_meta_data, True, 'get_meta_data should return a dictionary with a name property in it')
    eq_(isinstance(beer_meta_data['name'], basestring), True, 'the parameter for name in metadata should be a string')
    eq_(beer_meta_data['name'], '90 Minute IPA', 'the parameter for name in metadata should be "90 Minute IPA"')


    eq_('id' in beer_meta_data, True, 'get_meta_data should return a dictionary with an id in it')
    eq_(isinstance(beer_meta_data['id'], (int, long)), True, 'the parameter for id in metadata should be an int')
    eq_(beer_meta_data['id'], test_beer_id, 'the parameter for name in metadata should be %s' % test_beer_id)

    eq_('image_url' in beer_meta_data, True, 'get_meta_data should return a dictionary with an image_url property in it')
    eq_(isinstance(beer_meta_data['image_url'], basestring), True, 'the parameter for image_url in metadata should be a string')
    eq_(beer_meta_data['image_url'], 'http://cdn.beeradvocate.com/im/beers/2093.jpg', 'the parameter for image_url in metadata should be a http://cdn.beeradvocate.com/im/beers/2093.jpg')


  def test_get_next_recommendation(self):
    suggested_beer = database.get_next_recommendation(65)
    eq_(type(suggested_beer) is dict, True, 'get_next_recommendation should return a dictionary of a suggested beer')


  def test_get_next_recommendation_content(self):
    suggested_beer = database.get_next_recommendation(17060)
    suggested_beer_name = suggested_beer['name']
    eq_(len(suggested_beer_name) > 0, True, 'the resultant dictionary of get_next_recommendation should contain a name property')
