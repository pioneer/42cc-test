import unittest

from django.conf import settings
from django.test.client import Client

from common.models import HttpRequestLogRecord


class WelcomeTo42CcTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 302)
        
        self.client.login(username='pioneer', password='123456')
        response = self.client.get('/')
        self.assertTrue("Serge Tarkovski" in response.content)
        self.assertTrue("serge.tarkovski@gmail.com" in response.content)
        self.assertTrue("Cell phone: +380-63-192-4340" in response.content)
        self.assertTrue("Pinocchio is a fictional character that" in response.content)
    
    def test_login(self):
        self.client.logout()
        
        response = self.client.get('/login/')
        self.failUnlessEqual(response.status_code, 200)
        
        response = self.client.post('/login/', {'username': 'pioneer', 'password': '123'})
        self.failUnlessEqual(response.status_code, 200)
        self.assertTrue("Your username and password didn't match. Please try again." in response.content)
        
        response = self.client.post('/login/', {'username': 'abc', 'password': '123456'})
        self.failUnlessEqual(response.status_code, 200)
        self.assertTrue("Your username and password didn't match. Please try again." in response.content)
        
        response = self.client.post('/login/', {'username': 'pioneer', 'password': '123456'})
        self.failUnlessEqual(response.status_code, 302)
        
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.context['user'].username, 'pioneer')
        
        response = self.client.get('/logout/')
        self.failUnlessEqual(response.status_code, 302)
        response = self.client.get('/login/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
    
    def test_middleware(self):
        self.client.logout()
        
        response = self.client.get('/')
        
        record = HttpRequestLogRecord.objects.get_last_record()
        self.failUnlessEqual(record.url, "/")
        self.failUnlessEqual(record.method, "GET")
        self.failUnlessEqual(record.status_code, 302)
        
        response = self.client.get('/login/')
        
        record = HttpRequestLogRecord.objects.get_last_record()
        self.failUnlessEqual(record.url, "/login/")
        self.failUnlessEqual(record.method, "GET")
        self.failUnlessEqual(record.status_code, 200)
        
        response = self.client.post('/login/', {'username': 'pioneer', 'password': '123456'})
        
        record = HttpRequestLogRecord.objects.get_last_record()
        self.failUnlessEqual(record.url, "/login/")
        self.failUnlessEqual(record.method, "POST")
        self.failUnlessEqual(record.status_code, 302)
        
        response = self.client.get('/')
        
        record = HttpRequestLogRecord.objects.get_last_record()
        self.failUnlessEqual(record.url, "/")
        self.failUnlessEqual(record.method, "GET")
        self.failUnlessEqual(record.status_code, 200)
        
        response = self.client.get('/logout/')
        
        record = HttpRequestLogRecord.objects.get_last_record()
        self.failUnlessEqual(record.url, "/logout/")
        self.failUnlessEqual(record.method, "GET")
        self.failUnlessEqual(record.status_code, 302)
