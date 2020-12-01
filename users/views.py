import os
import jwt
import json 
from django.views import View 
from django.http import HttpResponse, JsonResponse 
from django.shortcuts import render,redirect
from django.contrib import auth 
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model 
from django.core.exceptions import ValidationError 
from django.core.validators import validate_email 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token 
from .text import message
from kudoc.my_settings import EMAIL
# Create your views here.
def home(request):
    return render(request,'home.html')

def main(request):
    return render(request,'main.html')

def login(request):
     return render(request,'account/login.html')

def logout(request):
     return render(request,'account/logout.html')

# def signup(request): # 메일 주소 전달받음 -> 메일 인증 
#     email = request.POST.get('e_mail')

#     return HttpResponse(email)

class SignUpView(View):

    def post(self, request):
        data = request.POST['e_mail']
        if User.objects.filter(email = data).exists():
                # 이미 인증 받은 메일의 경우 
            return JsonResponse({"message":"EXISTS_EMAIL"},status=400)

        user = request.user
        user.email = data
        user.is_valid = False 
        user.save()

        try:
            validate_email(data)

            current_site = get_current_site(request)
            domain = current_site.domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            message_data = message(domain, uidb64,token)

            mail_title = " 이메일 인증을 완료해주세요 !"
            mail_to = data
            email = EmailMessage(mail_title,message_data, to = [mail_to])
            email.send()

            return JsonResponse({"message": "SUCCESS"}, status = 200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status = 400)
        except TypeError:
            return JsonResponse({"message": "INVALID_TYPE"}, status = 200)
        except ValidationError:
            return JsonResponse({"message": "VALIDATION_ERROR"}, status = 200)


class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)

            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()

                return redirect(EMAIL['REDIRECT_PAGE'])
            
            return JsonResponse({"message":"AUTH FAIL"}, status=400)

        except ValidationError:
            return JsonResponse({"message":"TYPE_ERROR"},status=400)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEY"},status=400)
