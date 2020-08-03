from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import logout, login, authenticate

from .models import GreenLeafUserProfile

from .forms import GreenLeafUserCreationForm


def logoutView(request):
    logout(request)
    return redirect('/register')


def loginView(request):
    args = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/user/' + str(user.id))
        args = {'error': 'Неверный логин или пароль'}
    return render(request, 'userprofile/login.html', args)


def profileViewWithId(request, userId):
    user = get_object_or_404(User, id=userId)
    user_profile = get_object_or_404(GreenLeafUserProfile, id=userId)
    args = {'greenLeafUser': user,
            'userProfile': user_profile}
    return render(request, 'userprofile/userProfile.html', args)


class RegisterView(View):
    form_class = GreenLeafUserCreationForm
    template_name = 'userprofile/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password1'],
                                            first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'])
            userProfile = GreenLeafUserProfile.objects.create(id=user.id,
                                                              user=user,
                                                              city='',
                                                              phone='')
            userProfile.save()
            return redirect('/user/' + str(user.id))

        return render(request, self.template_name, {'form': form})
