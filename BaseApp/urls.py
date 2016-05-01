from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^conversation/', include('conversation.urls')),


    url(r'^home/$', views.home, name='home'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', views.login, name='login'),

    # user pages
    url(r'^user/(?P<user_id>\d+)/$', views.user_profile, name='user_profile'),

    url(r'^conversations/$', views.conversation_list, name='conversations_list'),


    # business pages
    url(r'^business/(?P<business_id>\d+)/$', views.business_profile, name='business_profile'),
]
