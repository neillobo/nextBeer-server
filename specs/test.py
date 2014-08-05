# loading depedencies
import unittest, sys, os

# list of nose.tools can be found at https://nose.readthedocs.org/en/latest/testing_tools.html
from nose.tools import eq_, raises, timed, with_setup

# in order to access objects in server.py
sys.path.insert(0, os.getcwd())
import server

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

  def test_get_nearest_beers(self):
    associated_beer_list = server.get_nearest_beers(3)
    eq_(type(associated_beer_list) is list, False, 'get_nearest_beers should return a list')

  def test_get_next_recommendation(self):
    suggested_beer = server.get_next_recommendation(1)
    eq_(type(suggested_beer) is dict, True, 'get_next_recommendation should return a dictionary of a suggested beer')

  def test_get_next_recommendation_content(self):
    suggested_beer = server.get_next_recommendation(1)
    suggested_beer_name = suggested_beer['name']
    eq_(len(suggested_beer_name) > 0, True, 'the resultant dictionary of get_next_recommendation should contain a name property')
