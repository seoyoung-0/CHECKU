from django.conf.urls import url
from django.urls import path,include 
from . import views

urlpatterns = [
    path('users/', include('allauth.urls')),
    path('login/', views.login, name = "login"),
    path('logout/', views.logout, name = "logout"),
    # path('signup/', views.signup, name='signup'), # 메일입력받아서 인증메일 보내기 
    # path('activate/<str:uidb64>/<str:token>/',views.activate, name="activate")

]