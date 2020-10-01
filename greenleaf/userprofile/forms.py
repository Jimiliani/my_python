from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import Input
from django.utils.translation import gettext_lazy as _

from userprofile.models import Profile, Message, ProfilePost


class GreenLeafUserCreationForm(UserCreationForm):
    class Meta:
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Адрес электронной почты'
        self.fields['email'].required = True
        self.fields['first_name'].label = 'Имя'
        self.fields['first_name'].required = True
        self.fields['last_name'].label = 'Фамилия'
        self.fields['last_name'].required = True


class GreenLeafUserProfileChangeForm(forms.ModelForm):
    class Meta:
        fields = ('city', 'phone', 'profile_picture')
        model = Profile
        widgets = {
            'profile_picture': Input(attrs={'type': 'file', 'name': 'profile_picture',
                                            'accept': 'image/*', 'id': 'profile_picture'})
        }
        labels = {
            'profile_picture': _('Выберите изображение')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].label = 'Город'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['profile_picture'].label = 'Фотография профиля'


class PostCreationForm(forms.ModelForm):
    class Meta:
        fields = ('post_text',)
        model = ProfilePost

