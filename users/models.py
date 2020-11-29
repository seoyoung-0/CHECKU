from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=200, unique=True)
    is_active= models.BooleanField(default=False)

    def __str__(self):
        return self.name