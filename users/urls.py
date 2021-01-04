from django.conf.urls import url
from django.urls import path,include 
from . import views
from .views import kakao_login,kakao_callback,SignUpView, Activate,NoticeList,SubscribeView

urlpatterns = [
    path('users/', include('allauth.urls')),
    path('', views.login, name = "login"),
    path('logout/', views.logout, name = "logout"),
    path('login/kakao/', kakao_login, name='kakao_login'),
    path('login/kakao/callback/', kakao_callback, name='kakao_callback'),
    path('signup/', SignUpView.as_view(), name="signup"), # 메일입력받아서 인증메일 보내기 
    path('activate/<str:uidb64>/<str:token>/',Activate.as_view(),name="activate"),
    # path('main/', NoticeList.as_view(), name = "main"),
    path('main/subscribe/<int:notice_id>/', SubscribeView.as_view(), name="subscribe"),
]