from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.utils import timezone 
from django.conf import settings
from django.db import models
from multiselectfield import MultiSelectField

SUBSCRIPTION_CHOICES = (
        ('AC','Academic'), #학사 
        ('ST','Student'),#학생
        ('SC','Scolarship'),#장학
        ('IN','Industry'),#산학
        ('EM','Employment'),#취창업
        ('CV','Corona'),#코로나
        ('IT', 'International'),#국제 
)

class User(models.Model):
    username = models.CharField(max_length=50, unique=False)
    email = models.EmailField(max_length=200, unique=True)
    is_active= models.BooleanField(default=True)
    subscription_list = MultiSelectField(choices = SUBSCRIPTION_CHOICES)

    # 구독- multiplechoice 로 바꾸기 
    def __str__(self):
        return self.username 


class Notice(models.Model):
    title = models.CharField(max_length=50, unique=True),
    subscribed = models.ManyToManyField(User)