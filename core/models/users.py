from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_seeker = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
