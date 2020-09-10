from django.db import models
from uuid import uuid4


# Create your models here.
class Log(models.Model):
    """Модель лога"""
    # генерится само
    id = models.UUIDField(unique=True, default=uuid4, primary_key=True, db_index=True)
    # request.META
    request_method = models.CharField(max_length=155, null=True, blank=True)
    remote_addr = models.CharField(max_length=155, null=True, blank=True)
    path_info = models.TextField(null=True, blank=True)
    content_type = models.CharField(max_length=155, null=True, blank=True)
    http_user_agent = models.CharField(max_length=155, null=True, blank=True)
    # request
    user = models.CharField(max_length=155, null=True, blank=True)
    # response
    status_code = models.PositiveSmallIntegerField(null=True, blank=True)
    reason_phrase = models.CharField(max_length=155, null=True, blank=True)
    user_errors = models.TextField(null=True, blank=True)
    # генерирую самостоятельно
    begin_date = models.DateTimeField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    exc_type = models.CharField(max_length=155, null=True, blank=True)
    exc_value = models.TextField(null=True, blank=True)
    exc_traceback = models.TextField(null=True, blank=True)
