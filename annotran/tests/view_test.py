import unittest

from pyramid import testing
import unittest



def dummy_request():
    return testing.DummyRequest()


class BaseTest(unittest.TestCase):
    def setUp(self):
        print()