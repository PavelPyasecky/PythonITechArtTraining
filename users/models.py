from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField('email address', unique=True, blank=True)
    birthday = models.DateField('%m/%d/%y')
    is_active = models.BooleanField(default=False)
    activate_time = models.DateTimeField(default=None, null=True)
    link_time = models.DateTimeField(default=None, null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                primary_key=True)


class Game(models.Model):
    id = models.IntegerField(primary_key=True)
    reporter = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=CustomUser)
