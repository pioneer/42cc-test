from django.db import models


class HttpRequestLogRecordManager(models.Manager):
    """
    Custom manager that adds getting last record functionality
    """
    def get_last_record(self):
        """
        Get last HTTP record
        """
        try:
            record = self.all().order_by('-id')[0]
        except IndexError:
            record = None
        return record
