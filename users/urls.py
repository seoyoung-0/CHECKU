from django.conf.urls import url
from django.urls import path, include
from . import views
from .views import kakao_login, kakao_callback, SignUpView, Activate, NoticeList, SubscribeView

urlpatterns = [
    path('users/', include('allauth.urls')),
    path('', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('login/kakao/', kakao_login, name='kakao_login'),
    path('login/kakao/callback/', kakao_callback, name='kakao_callback'),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('activate/<str:uidb64>/<str:token>/',
         Activate.as_view(), name="activate"),
    path('main/subscribe/<int:notice_id>/',
         SubscribeView.as_view(), name="subscribe"),
    path('success/', views.success, name="success"),
    path('updated/', views.send_notification, name="send_notification"),
]
