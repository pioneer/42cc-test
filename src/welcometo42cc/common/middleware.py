from common.models import HttpRequestLogRecord


class HttpLoggerMiddleware(object):
    """
    Middleware to log all HTTP requests in database
    """

    def process_response(self, request, response):
        """
        Creates a log record for every HTTP request
        """
        HttpRequestLogRecord.objects.create(url=request.get_full_path(), \
                                            method=request.method, \
                                            status_code=response.status_code)
        return response
