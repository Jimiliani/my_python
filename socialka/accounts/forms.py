from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'password1',
            'password2'
        ]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        us = authenticate(username=user.username, password=user.password)
        if us is not None:
            return True
        else:
            return False


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name'
        ]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user']
