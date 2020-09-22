from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from userprofile.models import Profile, Message


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].label = 'Город'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['profile_picture'].label = 'Фотография профиля'


class MessageCreationForm(forms.ModelForm):
    class Meta:
        fields = ('text',)
        model = Message

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = 'Текст сообщения'
