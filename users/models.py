from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
from django.utils import timezone
from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=155, null=True, blank=True)
    last_name = models.CharField(max_length=155, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_full_name(self):
        if not (self.first_name and self.last_name):
            return self.email
        else:
            return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        if not self.first_name:
            return self.email
        else:
            return self.first_name

    def __str__(self):
        return self.email
