from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import InfluencerProfile


class CreateProfileForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UpdateProfileForm(ModelForm):
    class Meta:
        model = InfluencerProfile
        fields = ['bio', 'ig_link']
