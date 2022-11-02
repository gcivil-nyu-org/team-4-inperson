from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login


@receiver(pre_social_login)
def pre_social_login_receiver(request, sociallogin, **kwargs):
    print(type(sociallogin.user), kwargs)
