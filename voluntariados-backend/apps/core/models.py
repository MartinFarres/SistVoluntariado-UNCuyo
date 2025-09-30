from django.db import models
from django.contrib.auth import get_user_model
from allauth.account.signals import user_logged_in


def user_logged_in_callback(request, user, **kwargs):
    print("User logged in!")
    print(request)
    print(user)

user = get_user_model()
user_logged_in.connect(user_logged_in_callback, sender=user)
