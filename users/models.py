from django.utils import timezone 
from django.conf import settings
from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User,AbstractUser
from django.contrib.auth.models import UserManager as DefaultUserManager

#이름, 이메일, is_active, 구독 리스트 

class UserManager(DefaultUserManager):
    def get_or_create_kakao_user(self,user_pk,extra_data):
        user = User.objects.get(pk=user_pk)
        user.username = extra_data['name']
        user.save()

        return user

SUBSCRIPTION_CHOICES = (
        ('AC','Academic'), #학사 
        ('ST','Student'),#학생
        ('SC','Scolarship'),#장학
        ('IN','Industry'),#산학
        ('EM','Employment'),#취창업
        ('CV','Corona'),#코로나
        ('IT', 'International'),#국제 
)

# class User(models.Model):
#     username = models.CharField(max_length=50, unique=False,blank=True)
#     email = models.EmailField(max_length=200, unique=True,blank=True)
#     is_active= models.BooleanField(default=False,blank=False)
#     #subscription_list = MultiSelectField(choices = SUBSCRIPTION_CHOICES,blank=True)
    
#     def __str__(self):
#         return self.username 

# class MyUser(AbstractUser):
#     username = models.CharField(max_length=50, unique=False,blank=True)
#     email = models.EmailField(max_length=200, unique=True,blank=True)
#     password = models.CharField(max_length=20, null=True, default='')
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#     is_active= models.BooleanField(default=False,blank=False)
#     subscription_list = MultiSelectField(choices = SUBSCRIPTION_CHOICES,blank=True)
    
#     def __str__(self):
#         return self.username 

class Notice(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user',null=True)
    title = models.CharField(max_length=20,null=True)
    subscribed = models.ManyToManyField(User, related_name='subscribed_menu', blank=True)

    class Meta:
        ordering =['title']

    def __str__(self):
        return str(self.title)
