from urllib.request import urlopen
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from . import models as m
from django.core.files.base import ContentFile
from social.utils import slugify


class ProfileAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        '''
        Check for extra user data and save the desired fields.
        '''
        data = sociallogin.account.extra_data
        user = sociallogin.user
        print("LOGS: Caught the signal -> Printing extra data of the account: \n" + str(data))
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']

        try:
            appuser = m.AppUser.objects.get(user=user)

        except:
            appuser = m.AppUser()
            user.appuser = appuser


        url = "http://graph.facebook.com/%s/picture?type=large" % user.socialaccount_set.filter(provider='facebook')[0].uid
        avatar = urlopen(url)
        appuser.gender = data['gender']
        try:
            appuser.image.delete()
            appuser.image.save('avatar.jpg',
                            ContentFile(avatar.read()))
        except:
            appuser.image.save('avatar.jpg',
                        ContentFile(avatar.read()))
        appuser.save()

