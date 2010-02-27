import unittest

from django.conf import settings
from django.test.client import Client

from common.models import HttpRequestLogRecord

import html5lib
from html5lib import treebuilders, treewalkers, serializer
from html5lib.filters import sanitizer


def html5_parse_and_get_form_tags(s):
    """
    Parses HTML page and extracts form tags from it
    """
    p = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))
    dom_tree = p.parse(s)
    walker = treewalkers.getTreeWalker("dom")
    stream = walker(dom_tree)
    s = serializer.htmlserializer.HTMLSerializer(omit_optional_tags=False)
    tags = s.serialize(stream)

    form_tags = []

    for tag in tags:
        if any(tag.startswith(s) for s in ("<form", "</form", "<input")):
            form_tags.append(tag)
        if tag.startswith("<textarea"):
            form_tags.append("%s%s%s" % (tag, tags.next(), tags.next()))
    
    return form_tags


class WelcomeTo42CcTest(unittest.TestCase):
    """
    Tests for the project
    """

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

    def test_context(self):
        response = self.client.get('/login/')

        # context does not allow to use just 'xxx' in var syntax
        try:
            settings = response.context['settings']
        except KeyError:
            settings = None

        self.failIfEqual(settings, None)
        self.failUnlessEqual(settings.SECRET_KEY, "(##miaswe4+szpto%a9jku&b+=5v1y@63r%y%i37qk97hzvlzn")
        self.failUnlessEqual(settings.ROOT_URLCONF, "welcometo42cc.urls")

    def test_form_and_reverse_order(self):
        self.client.logout()
        response = self.client.get('/form/')
        self.failUnlessEqual(response.status_code, 302)

        self.client.login(username='pioneer', password='123456')
        response = self.client.get('/form/')
        self.failUnlessEqual(response.status_code, 200)

        form_tags = html5_parse_and_get_form_tags(response.content)

        self.assertTrue(form_tags[0].startswith("<form"))
        self.assertTrue(form_tags[-1] == "</form>")
        self.assertFalse(any(t.startswith("<form") for t in form_tags[1:-1]))
        self.assertFalse(any(t == "</form>" for t in form_tags[1:-1]))

        self.assertTrue("action=/form/" in form_tags[0] or "action=." in form_tags[0])

        def is_input(tag, name, value):
            return tag.startswith("<input") and "name=%s" % name in tag \
                   and "type=text" in tag \
                   and "value=%s" % value in tag

        def is_textarea(tag, name, value):
            return tag.startswith("<textarea") and tag.endswith("</textarea>") \
                   and "name=%s" % name in tag and value in tag

        self.assertTrue(is_input(form_tags[6], "first_name", "Serge"))
        self.assertTrue(is_input(form_tags[5], "last_name", "Tarkovski"))
        self.assertTrue(is_input(form_tags[4], "birthdate", "1980-06-15"))
        self.assertTrue(is_textarea(form_tags[3], "biography", "Pinocchio is a fictional character that"))
        self.assertTrue(is_input(form_tags[2], "email", "serge.tarkovski@gmail.com"))
        self.assertTrue(is_textarea(form_tags[1], "contacts", "Cell phone: +380-63-192-4340"))

        response = self.client.post('/form/', {'first_name': 'Vasya', \
                                               'last_name': 'Pupkin', \
                                               'birthdate': '1970-01-01', \
                                               'biography': 'The ancestor of the Pupkin\'s genus was a viking jarl Pupkur, who came to Russia in ancient times.', \
                                               'email': 'pupkin@pupkin.ru', \
                                               'contacts': 'Use rails'})
        self.failUnlessEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertTrue("Vasya Pupkin" in response.content)
        self.assertTrue("pupkin@pupkin.ru" in response.content)
        self.assertTrue("Use rails" in response.content)
        self.assertTrue("The ancestor of the Pupkin" in response.content)
        self.assertTrue("1 Jan 1970" in response.content)

        response = self.client.post('/form/', {'first_name': '', \
                                               'last_name': 'Pupkin', \
                                               'birthdate': '1970-01-012', \
                                               'biography': '', \
                                               'email': 'pupkin@', \
                                               'contacts': ''})
        self.failUnlessEqual(response.status_code, 200)
        self.assertTrue("This field is required" in response.content)
        self.assertTrue("Enter a valid date" in response.content)
        self.assertTrue("Enter a valid e-mail address" in response.content)

        # Roll back to initial data
        response = self.client.post('/form/', {'first_name': 'Serge', \
                                               'last_name': 'Tarkovski', \
                                               'birthdate': '1980-06-15', \
                                               'biography': 'Pinocchio is a fictional character that first appeared in 1883, in The Adventures of Pinocchio by Carlo Collodi.', \
                                               'email': 'serge.tarkovski@gmail.com', \
                                               'contacts': 'Cell phone: +380-63-192-4340'})
        self.failUnlessEqual(response.status_code, 302)

import os
from windmill.authoring import djangotest 

class TestProjectWindmillTest(djangotest.WindmillDjangoUnitTest):
    test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wmtests')
    browser = 'firefox'

