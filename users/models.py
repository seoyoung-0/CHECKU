from django.utils import timezone 
from django.conf import settings
from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser

SUBSCRIPTION_CHOICES = (
        ('AC','Academic'), #학사 
        ('ST','Student'),#학생
        ('SC','Scolarship'),#장학
        ('IN','Industry'),#산학
        ('EM','Employment'),#취창업
        ('CV','Corona'),#코로나
        ('IT', 'International'),#국제 
)
class User(AbstractUser):
    kakao_id=models.IntegerField(default=0)
    nickname = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=30, unique=True)
    active = models.BooleanField(default=False)

class Notice(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user',null=True)
    title = models.CharField(max_length=20,null=True)
    subscribed = models.ManyToManyField(User, related_name='subscribed_menu', blank=True)

    class Meta:
        ordering =['title']

    def __str__(self):
        return str(self.title)
