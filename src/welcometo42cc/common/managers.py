from django.db import models

class HttpRequestLogRecordManager(models.Manager):
    
    def get_last_record(self):
        try:
            record = self.all().order_by('-id')[0]
        except IndexError:
            record = None
        return record
