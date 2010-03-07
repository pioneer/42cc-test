from django.db import models
from django.contrib.auth.models import User

from common.managers import HttpRequestLogRecordManager

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


# Monkey-patching User model
User.add_to_class('biography', models.TextField(max_length=400, blank=True))
User.add_to_class('birthdate', models.DateField(null=True, blank=True))
User.add_to_class('contacts', models.TextField(max_length=400, blank=True))


class HttpRequestLogRecord(models.Model):
    """
    A representation of HTTP request log record
    """
    url = models.CharField(max_length=255)
    method = models.CharField(max_length=4)
    status_code = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)

    objects = HttpRequestLogRecordManager()

    def __unicode__(self):
        return self.url


class ModelLog(models.Model):
    """
    A representation of model create/update/delete log record
    """
    ACTIONS = (
        ('C', 'Create'),
        ('U', 'Update'),
        ('D', 'Delete')
    )
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    object_description = models.CharField(max_length=255)
    action = models.CharField(max_length=1, choices=ACTIONS)
    datetime = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "%s: <%s: %s>" % (self.get_action_display(), self.content_type, self.object_description)
