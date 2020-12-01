from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.utils import timezone 
from django.conf import settings
from django.db import models

# class UserManager(BaseUserManager):
#     def create_user(self, username, email=None, password=None, **extra_fields):
#             email = self.normalize_email(email)
#             user = self.model(email=email, **extra_fields)
#             extra_fields.setdefault('is_superuser', False)
#             extra_fields.setdefault('is_admin', False)
#             user.set_password(password)
#             user.is_active=False
#             user.save(using=self._db)
#             return user

#     def create_superuser(self, username, email=None, password=None,**extra_fields):
#             extra_fields.setdefault('is_superuser', True)
#             extra_fields.setdefault('is_admin', True)
#             superuser = self.create_user(username,email,password,**extra_fields)
#             superuser.is_active=True
#             superuser.save(using=self._db)
#             return superuser

# class MyUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(
#         verbose_name ='Email_address',
#         max_length = 255,
#         unique=True,
#     )
#     username = models.CharField(
#         verbose_name='Username',
#         max_length = 30,
#         unique=True,
#     )
#     is_active = models.BooleanField(
#         verbose_name='Is_active',
#         default = False,
#     )
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)

#     USERNAME_FIELD = 'username'
#     objects = UserManager()

class User(models.Model):
    username = models.CharField(max_length=50, unique=False)
    email = models.EmailField(max_length=200, unique=True)
    is_active= models.BooleanField(default=False)

    def __str__(self):
        return self.username 
