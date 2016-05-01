from django.shortcuts import render, get_object_or_404
from . import models as m
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from conversation.models import Conversation
#
# def index(request):
#     if request.user.is_authenticated():
#         return render(request, 'BaseApp/mybase.html')
#     else:
#         return render(request, 'BaseApp/login.html')


def get_element_by_id(_list, _id):
    for element in _list:
        if element.id == _id:
            return element
    return -1


def home(request):
    context = {}
    return news_feed(request)


def get_image_url(uid):
    return 'http://graph.facebook.com/%s/picture?width=100&height=100' % uid


def user_profile(request, user_id):
    p_user = get_object_or_404(User, id = user_id)
    socialaccount = SocialAccount.objects.get(user=p_user, provider="facebook")
    context = {
        "p_user": p_user,
        "socialaccount": socialaccount,
    }
    return render(request, 'BaseApp/user_profile.html', context)


def business_profile(request, business_id):
    p_business = get_object_or_404(m.Business, id = business_id)
    context = {
        "p_business": p_business,
    }
    return render(request, 'BaseApp/business_profile.html', context)


def login(request):
    context = {}
    if request.user.is_authenticated():
        return news_feed(request)
    else:
        return render(request, 'BaseApp/login.html', context)


def news_feed(request):
    posts = m.BasePost.objects.all()
    app_user = request.user
    context = {
        'posts': posts,
        'app_user': app_user,
    }
    return render(request, 'BaseApp/news_feed.html', context)


def add_post_like(post, user):
    try:
        like = m.PostLike.objects.get_or_create(
)
        like.post = post
        like.user = user
        like.save()
    finally:
        return


def add_post_comment(post, user, text):
    try:
        comment = m.Comment()
        comment.post = post
        comment.user = user
        comment.text = text
        comment.save()
    finally:
        return


def logout(request):
    return render(request, 'BaseApp/login.html')


def conversation_list(request):
    conversations = request.user.conversations.all()
    context = {
        "conversations": conversations,
    }
    return render(request, 'conversation/conversation_list.html', context)
