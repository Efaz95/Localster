from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import InfluencerProfile, BusinessProfile, Messages


class CreateProfileForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UpdateInfProfileForm(ModelForm):
    class Meta:
        model = InfluencerProfile
        fields = ['bio', 'ig_link', 'followers', 'city', 'state', 'zip_code']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class UpdateBisProfileForm(ModelForm):
    class Meta:
        model = BusinessProfile
        fields = ['business_name', 'street_address', 'city', 'state', 'zip_code']


class MessagesForm(ModelForm):
    class Meta:
        model = Messages
        fields = '__all__'
