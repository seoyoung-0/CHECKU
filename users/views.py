import os
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import auth 
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model 

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token 

# Create your views here.
def home(request):
    return render(request,'home.html')

def main(request):
    return render(request,'main.html')

def login(request):
     return render(request,'account/login.html')

def logout(request):
     return render(request,'account/logout.html')
