# loading depedencies
import unittest
# list of nose.tools can be found at https://nose.readthedocs.org/en/latest/testing_tools.html
from nose.tools import assert_equal, assert_not_equal, assert_raises

# load the stub script to test
# this is to be replaced with the actual functions later on
from stubs import dummyscript


def test_csv():
  beers = ["Dale's Pale Ale", "Sierra Nevada Pale Ale"]
  unittest = dummyscript.calculate_similarity(beers[0], beers[1])
  assert_equal(type(unittest),'number')
  # assert_equal(unittest,)

def setup_module(module):
    print ("") # this is to get a newline after the dots
    print ("setup_module before anything in this file")
