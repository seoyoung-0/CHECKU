from django.conf.urls import url
from django.urls import path,include 
from . import views
from .views import SignUpView, Activate

urlpatterns = [
    path('users/', include('allauth.urls')),
    path('login/', views.login, name = "login"),
    path('logout/', views.logout, name = "logout"),
    path('signup/', SignUpView.as_view(), name="signup"), # 메일입력받아서 인증메일 보내기 
    path('activate/<str:uidb64>/<str:token>/',Activate.as_view(),name="activate"),
    path('main/', views.main, name = "main"),

]