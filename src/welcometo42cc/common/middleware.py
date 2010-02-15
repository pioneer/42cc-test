from common.models import HttpRequestLogRecord

from django.http import HttpResponse

class HttpLoggerMiddleware(object):
    
    def process_response(self, request, response):
        HttpRequestLogRecord.objects.create(url=request.get_full_path(), \
                                            method=request.method, \
                                            status_code=response.status_code)
        return response