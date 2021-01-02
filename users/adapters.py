from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager 
from allauth.exceptions import ImmediateHttpResponse

class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin,form=None):
        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)
        return redirect('/') 
        # social_app_name = sociallogin.account.provider.upper()

        # if social_app_name == "KAKAO":
        #     User.objects.get_or_create_kakao_user(user_pk=user.pk, extra_data = extra_data)
        
        # print(dir(sociallogin))