from datetime import datetime
import time
import json
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework import status
from log.loggers import LogObject, ErrorLogObject


class LoggingMiddleware(MiddlewareMixin):
    ignored_paths = ['/admin', '/static', '/favicon.ico']
    begin_date = None
    start_time = None

    def process_request(self, request):
        self.begin_date = str(datetime.now())
        self.start_time = time.time()

    def process_response(self, request, response):
        duration = round(time.time() - self.start_time, 3)

        if request.path_info.startswith(tuple(self.ignored_paths)):
            return response

        if response.status_code == 500:
            return response

        if response.__class__.__name__ == 'JsonResponse':
            if 200 <= response.status_code <= 300:
                log = LogObject(request=request, response=response, duration=duration, begin_date=self.begin_date)
                result = log.format_request
                result.update(log.format_response)
                log = log.to_db(result)
                response_content = json.loads(response.content.decode(response.charset))
                return JsonResponse({
                    'guid': str(log.id),
                    'timestamp': str(log.begin_date),
                    'status': 'ok',
                    'details': response_content
                }, safe=False)
            elif 300 <= response.status_code <= 400:
                log = LogObject(request=request, response=response, duration=duration, begin_date=self.begin_date)
                result = log.format_request
                result.update(log.format_response)
                log = log.to_db(result)
                response_content = json.loads(response.content.decode(response.charset))
                return JsonResponse({
                    'guid': str(log.id),
                    'timestamp': str(log.begin_date),
                    'status': 'error',
                    'details': response_content
                }, safe=False, status=status.HTTP_400_BAD_REQUEST)

        else:
            log = LogObject(request=request, response=response, duration=duration, begin_date=self.begin_date)
            result = log.format_request
            result.update(log.format_response)
            log.to_db(result)
            return response

    def process_exception(self, request, exception):
        duration = round(time.time() - self.start_time, 3)
        log = ErrorLogObject(request, duration, self.begin_date, exception)
        result = log.format_request
        result.update(log.format_exception)
        log.to_db(result)
