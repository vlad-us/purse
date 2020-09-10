import sys
import traceback
from .models import Log


class BaseLogObject(object):
    def __init__(self, request, duration, begin_date):
        self.request = request
        self.duration = duration
        self.begin_date = begin_date

    @property
    def format_request(self):
        meta_keys = ['REQUEST_METHOD', 'COMPUTERNAME', 'REMOTE_ADDR', 'PATH_INFO', 'CONTENT_TYPE', 'HTTP_USER_AGENT']
        result = {key.lower(): value for key, value in self.request.META.items() if key in meta_keys}
        result['begin_date'] = self.begin_date
        result['duration'] = self.duration
        try:
            result['user'] = str(self.request.user)
        except AttributeError:
            result['user'] = None
        return result

    def to_db(self, log):

        instance = Log(
            begin_date=log.get('begin_date', None),
            content_type=log.get('content_type', None),
            duration=log.get('duration', None),
            exc_traceback=log.get('exc_traceback', None),
            exc_type=log.get('exc_type', None),
            exc_value=log.get('exc_value', None),
            http_user_agent=log.get('http_user_agent', None),
            path_info=log.get('path_info', None),
            reason_phrase=log.get('reason_phrase', None),
            remote_addr=log.get('remote_addr', None),
            request_method=log.get('request_method', None),
            status_code=log.get('status_code', None),
            user=log.get('user', None),
            user_errors=log.get('user_errors', None)
        )
        instance.save()
        return instance


class LogObject(BaseLogObject):
    def __init__(self, request, response, duration, begin_date):
        super(LogObject, self).__init__(request, duration, begin_date)
        self.response = response

    @property
    def format_response(self):
        result = {
            'status_code': self.response.status_code,
            'reason_phrase': self.response.reason_phrase,
            'exc_type': None,
            'exc_value': None,
            'exc_traceback': None
        }

        if hasattr(self.response, 'user_errors'):
            result['user_errors'] = self.response.user_errors
        else:
            result['user_errors'] = None

        return result


class ErrorLogObject(BaseLogObject):
    def __init__(self, request, duration, begin_date, exception):
        super(ErrorLogObject, self).__init__(request, duration, begin_date)
        self.exception = exception

    @property
    def format_exception(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb = [i.rstrip().lstrip() for i in tb]
        exc_traceback = '\n'.join(tb)
        result = {
            'exc_type': str(exc_type),
            'exc_value': str(exc_value),
            'exc_traceback': str(exc_traceback),
            'status_code': '500',
            'reason_phrase': 'Internal server error',
            'user_errors': None
        }
        return result