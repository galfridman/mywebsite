from django.shortcuts import render, get_object_or_404
from . import models as m
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User


def user_profile(request, user_id):
    p_user = get_object_or_404(User, id=user_id)
    socialaccount = SocialAccount.objects.get(user=p_user, provider="facebook")
    context = {
        "p_user": p_user,
        "socialaccount": socialaccount,
    }
    return render(request, 'UserApp/profile.html', context)
