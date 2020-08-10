from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import logout, login, authenticate

from .models import GreenLeafUserProfile, PostProfile

from .forms import GreenLeafUserCreationForm, GreenLeafUserProfileChangeForm


def logoutView(request):
    logout(request)
    return redirect('/login')


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


def profileViewWithId(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(GreenLeafUserProfile, id=user_id)
    args = {'greenLeafUser': user,
            'userProfile': user_profile}
    return render(request, 'userprofile/userProfile.html', args)


def friendsView(request):
    return render(request, 'userprofile/friends.html')


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
            return redirect('userprofile:login')

        return render(request, self.template_name, {'form': form})


class SettingsView(View):
    form_class = GreenLeafUserProfileChangeForm
    template_name = 'userprofile/settings.html'

    def get(self, request, *args, **kwargs):
        userProfile = get_object_or_404(GreenLeafUserProfile, id=request.user.id, user=request.user)
        form = self.form_class(request.POST, instance=userProfile)
        return render(request, self.template_name, {'form': form,
                                                    'userProfile': userProfile})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        userProfile = get_object_or_404(GreenLeafUserProfile, id=request.user.id, user=request.user)
        if form.is_valid():
            userProfile.city = form.cleaned_data['city']
            userProfile.phone = form.cleaned_data['phone']
            # userProfile.profile_picture = form.cleaned_data['profile_picture']
            userProfile.save()
            return redirect('/user/' + str(request.user.id))
        return render(request, self.template_name,
                      {'form': form,
                       'error': 'Произошла ошибка. Скорее всего выбранный формат фотографий не поддерживается.',
                       'userProfile': userProfile})
