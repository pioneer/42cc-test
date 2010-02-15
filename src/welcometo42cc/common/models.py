from django.db import models
from django.contrib.auth.models import User

from common.managers import HttpRequestLogRecordManager

# Monkey-patching User model
User.add_to_class('biography', models.TextField(max_length=400, blank=True))
User.add_to_class('birthdate', models.DateField(null=True, blank=True))
User.add_to_class('contacts', models.TextField(max_length=400, blank=True))


class HttpRequestLogRecord(models.Model):
    url = models.CharField(max_length=255)
    method = models.CharField(max_length=4)
    status_code = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
    
    objects = HttpRequestLogRecordManager()
    
    def __unicode__(self):
        return self.url