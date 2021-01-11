import os
import jwt
import json
import urllib
import requests
from django.views import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from urllib.parse import urlparse
from django.utils import six
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from .text import message
from django.contrib.auth import login as django_login
from kudoc.my_settings import EMAIL,app_rest_api_key
from .models import Notice, User


def login(request):

    return render(request, 'account/login.html')


def logout(request):
    return render(request, 'account/logout.html')


def kakao_login(request):
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )

def kakao_callback(request):
    code = request.GET.get("code", None)
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"
    url = "https://kauth.kakao.com/oauth/token"
    headers = {
        'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'
    }
    body = {
        'grant_type': 'authorization_code',
        'client_id': app_rest_api_key,
        'redirect_uri': redirect_uri,
        'code': code
    }
    token_kakao_response = requests.post(url, headers=headers, data=body)
    access_token = json.loads(token_kakao_response.text).get('access_token')

    url = 'https://kapi.kakao.com/v2/user/me'

    headers = {
        'Authorization': f'Bearer {access_token}',
        # 'Content-type' : 'application/x-www-form-urlencoded; charset=utf-8'
    }
    kakao_response = requests.get(url, headers=headers)
    kakao_response = json.loads(kakao_response.text)

    # 사용자 존재할 때
    if User.objects.filter(kakao_id=kakao_response['id']).exists():
        user = User.objects.get(kakao_id=kakao_response['id'])
        jwt_token = jwt.encode({'id': user.kakao_id},
                               'checku', algorithm='HS256')
        print(user.is_authenticated)
        if user.is_authenticated:
            django_login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend",)
            return redirect("http://127.0.0.1:8000/main")

    # 처음 로그인 하는 User 추가
    User(
        kakao_id=kakao_response['id'],
        nickname=kakao_response['properties']['nickname'],
        active=False
    ).save()
    user = User.objects.get(kakao_id=kakao_response['id'])
    m_token = jwt.encode({'id': user.kakao_id}, 'checky', algorithm='HS256')
    if user.is_authenticated:
        django_login(
            request,
            user,
            backend="django.contrib.auth.backends.ModelBackend",)
        return redirect("http://127.0.0.1:8000/main")


class NoticeList(View):
    model = Notice
    template_name = 'main.html'

    def get(self, request):
        notice_list = Notice.objects.all()
        return render(request, 'main.html', {'notice_list': notice_list})


class SubscribeView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'notice_id' in kwargs:
                notice_id = kwargs['notice_id']
                notice = Notice.objects.get(pk=notice_id)
                user = request.user
                if user in notice.subscribed.all():
                    notice.subscribed.remove(user)
                else:
                    notice.subscribed.add(user)
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)

# class SubscribedList(View):
#     template_name = 'admin.html'
#     def get(self, request):
#         queryset = user.subscribed.all()

#     def get_queryset(self):
#         queryset = user.subscribed.all()
#         return queryset
# # user 별 구독한 모델 가져오기


# 메일인증
class SignUpView(View):

    def post(self, request):
        data = request.POST['e_mail']
        if User.objects.filter(email=data).exists():
            # 이미 인증 받은 메일의 경우
            return redirect("http://127.0.0.1:8000/main")

        user = request.user
        user.email = data
        user.valid = True
        user.save()

        try:
            validate_email(data)

            current_site = get_current_site(request)
            domain = current_site.domain  # 메일 인증 링크 전달시 전달되는 도메인
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            message_data = message(domain, uidb64, token)

            mail_title = " 이메일 인증을 완료해주세요 !"
            mail_to = data
            email = EmailMessage(mail_title, message_data, to=[mail_to])
            email.send()

            return HttpResponseRedirect("https://kumail.konkuk.ac.kr/adfs/ls/?lc=1042&wa=wsignin1.0&wtrealm=urn%3afederation%3aMicrosoftOnline")

            # return JsonResponse({"message": "SUCCESS"}, status = 200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)
        except TypeError:
            return JsonResponse({"message": "INVALID_TYPE"}, status=200)
        except ValidationError:
            return JsonResponse({"message": "VALIDATION_ERROR"}, status=200)


class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()

                return redirect(EMAIL['REDIRECT_PAGE'])

            return JsonResponse({"message": "AUTH FAIL"}, status=400)

        except ValidationError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)
