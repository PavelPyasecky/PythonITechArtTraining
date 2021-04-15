from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    birthday = models.DateField('%m/%d/%y')
    is_active = models.BooleanField(default=False)
    activate_date = models.DateTimeField(default=now)
