from django.db import models
from django.contrib.auth.models import User

from common.managers import HttpRequestLogRecordManager

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.db.models import signals


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
        return "%s: <%s: %s>" % (self.get_action_display(), self.content_type,\
                                 self.object_description)


def process_model_pre_change(sender, **kwargs):
    instance = kwargs['instance']
    if not isinstance(instance, ModelLog): # Do not record ModelLog changes to
                                           # avoid recursion
        instance._modellog_action = "C" if not getattr(instance, 'pk', None)\
                                        else "U"


def process_model_post_change(sender, **kwargs):
    instance = kwargs['instance']
    action = getattr(instance, '_modellog_action', None)
    if not isinstance(instance, ModelLog) and action in ("C", "U") \
       and type(instance.pk) == int: # Avoid logging objects such as
                                     # django.contrib.sessions.models.Session,
                                     # due to it is hard to maintain non-int
                                     # primary keys with contenttypes
                                     # framework, taking into account current
                                     # simple educational task
        ModelLog.objects.create(content_object=instance, action=action,\
                                object_description=unicode(instance))


def process_model_delete(sender, **kwargs):
    instance = kwargs['instance']
    if not isinstance(instance, ModelLog) and type(instance.pk) == int:
        ModelLog.objects.create(content_object=instance, action="D",\
                                object_description=unicode(instance))


signals.pre_save.connect(process_model_pre_change)
signals.post_save.connect(process_model_post_change)
signals.pre_delete.connect(process_model_delete)
