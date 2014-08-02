# loading depedencies
import unittest, sys

# list of nose.tools can be found at https://nose.readthedocs.org/en/latest/testing_tools.html
from nose.tools import assert_equal, assert_not_equal

# in order to access objects in server.py
sys.path.insert(0, '../')
import server

class Unit_Test():

  @classmethod
  def setup_class(klass):
    print "running unit tests for: ", klass

  def test_recommend(self):
    result = server.get_recommendation('something')
    assert_equal(result['beer_id'], 123)

  def test_somethingelse(self):
    result = server.get_recommendation('something')
    assert_not_equal(1234, 123)

  def test_somethingelse2(self):
    result = server.get_recommendation('22222')
    assert_not_equal(1455, 123)

  def test_somethingelse3(self):
    result = server.get_recommendation('22222')
    assert_not_equal(dfdsff, 123)

