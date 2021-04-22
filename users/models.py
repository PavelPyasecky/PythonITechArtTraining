from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField('email address', unique=True, blank=True)
    birthday = models.DateField('%m/%d/%y')
    is_active = models.BooleanField(default=False)
    activate_time = models.DateTimeField(default=None, null=True)
    link_time = models.DateTimeField(default=None, null=True)
