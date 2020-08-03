from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from userprofile.models import GreenLeafUserProfile


class GreenLeafUserCreationForm(UserCreationForm):
    class Meta:
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email Address'
        self.fields['email'].required = True
        self.fields['first_name'].label = 'First name'
        self.fields['first_name'].required = True
        self.fields['last_name'].label = 'Last name'
        self.fields['last_name'].required = True


class GreenLeafUserProfileChangeForm(forms.ModelForm):
    class Meta:
        fields = ('city', 'phone', 'profile_picture')
        model = GreenLeafUserProfile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].label = 'City'
        self.fields['phone'].label = 'Phone'
        self.fields['profile_picture'].label = 'Profile picture'
