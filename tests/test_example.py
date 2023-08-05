"""
File to test the pytest automation.

Author: Hana Turcke
"""

# import methods you want to test so they can be called below
from methods_to_test import my_method

def test_addition():
    # a trivial test (testing the built in + operator)
    assert 2 + 2 == 4

def test_my_method():
    # my_method is supposed to return the integer that it was passed
    # the assert statement is saying "ok this should be true"
    assert my_method(2) == 2