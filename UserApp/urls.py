from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^show_user/(?P<user_id>\d+)/$', views.user_profile, name='user_profile'),

]