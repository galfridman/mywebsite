__author__ = 'Gal'
from . import models as m
from django import forms


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')
    info = forms.CharField(max_length=30, label='info')

    def signup(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        profile = m.AppUser()
        profile.user = user
        profile.info = self.cleaned_data['info']
        profile.save()
        user.profile = profile
        user.save()

class AppUserForm(forms.ModelForm):
    class Meta:
        model = m.AppUser
        fields = [
            'birthdate',
            'address',
            'image',
            'gender',
            '',
        ]

