import unittest

from django.conf import settings
from django.test.client import Client


class WelcomeTo42CcTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTrue("Serge Tarkovski" in response.content)
        self.assertTrue("serge.tarkovski@gmail.com" in response.content)
        self.assertTrue("Cell phone: +380-63-192-4340" in response.content)
        self.assertTrue("Pinocchio is a fictional character that" in response.content)
