import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import logout, login, authenticate

from .models import Profile, ProfilePost, Friendship, Message

from .forms import GreenLeafUserCreationForm, GreenLeafUserProfileChangeForm, MessageCreationForm, PostCreationForm


@login_required(login_url='/login/')
def logoutView(request):
    logout(request)
    return redirect('/login')


def loginView(request):
    args = {}
    if request.user.is_authenticated:
        return redirect('/user/' + str(request.user.id))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/user/' + str(user.id))
        args = {'error': 'Неверный логин или пароль'}
    return render(request, 'userprofile/login.html', args)


class ProfileViewWithPk(LoginRequiredMixin, View):
    login_url = '/login/'
    form_class = PostCreationForm
    template_name = 'userprofile/userProfile.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs.pop('user_id'))
        are_friends = 'None'
        if user != request.user:
            try:
                Friendship.objects.get(friend1__user_id=min(int(user.id), int(request.user.id)),
                                       friend2__user_id=max(int(user.id), int(request.user.id)))
                are_friends = 'True'
            except Friendship.DoesNotExist:
                are_friends = 'False'
        print(request.GET)
        if request.GET and request.GET['request_type'] == 'are_friends':
            return JsonResponse(data={'are_friends': are_friends})

        user_profile = user.profile
        posts = ProfilePost.objects.filter(author=user_profile)[:10]
        form = self.form_class(request.POST)

        args = {'greenLeafUser': user,
                'userProfile': user_profile,
                'posts': posts,
                'form': form,
                'are_friends': are_friends}
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.POST['request_type'] == 'add_friend':
            print(request.POST['user'])
            try:
                friendship = Friendship.objects.get(
                    friend1__user_id=min(int(request.POST['user']), int(request.user.id)),
                    friend2__user_id=max(int(request.POST['user']), int(request.user.id)))
                friendship.friend1_agree = True
                friendship.friend2_agree = True
                friendship.save()
            except Friendship.DoesNotExist:
                if int(request.POST['user']) > int(request.user.id):
                    Friendship.objects.create(friend1=request.user.profile,
                                              friend2=User.objects.get(id=request.POST['user']).profile,
                                              friend1_agree=True)

                else:
                    Friendship.objects.create(friend1=User.objects.get(id=request.POST['user']).profile,
                                              friend2=request.user.profile,
                                              friend2_agree=True)
            return HttpResponse('success')
        elif request.POST['request_type'] == 'delete_friend':
            print(request.POST['user'])
            friendship = Friendship.objects.get(
                friend1__user_id=min(int(request.POST['user']), int(request.user.id)),
                friend2__user_id=max(int(request.POST['user']), int(request.user.id)))
            friendship.friend1_agree = False
            friendship.friend2_agree = False
            friendship.save()
            return HttpResponse('success')
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                ProfilePost.objects.create(author=request.user.profile,
                                           post_text=form.cleaned_data['post_text'])
                return JsonResponse(data={'text': form.cleaned_data['post_text']}, status=201)
            return HttpResponse(form=form, status=400)

    def patch(self, request, *args, **kwargs):
        body = json.loads(request.body.decode('utf-8'))
        post = get_object_or_404(ProfilePost, id=body['post_id'])
        if body['action_type'] == 'add':
            post.like.add(request.user.profile)
        elif body['action_type'] == 'remove':
            post.like.remove(request.user.profile)
        return JsonResponse(data={'is_liked': request.user.profile in post.like.all(),
                                  'count_of_likes': post.like.count()})


@login_required(login_url='/login/')
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
            User.objects.create_user(username=form.cleaned_data['username'],
                                     email=form.cleaned_data['email'],
                                     password=form.cleaned_data['password1'],
                                     first_name=form.cleaned_data['first_name'],
                                     last_name=form.cleaned_data['last_name'])
            return redirect('userprofile:login')

        return render(request, self.template_name, {'form': form})


class SettingsView(LoginRequiredMixin, View):
    login_url = '/login/'
    form_class = GreenLeafUserProfileChangeForm
    template_name = 'userprofile/settings.html'

    def get(self, request, *args, **kwargs):
        userProfile = get_object_or_404(Profile, user=request.user)
        form = self.form_class(request.POST, instance=userProfile)
        return render(request, self.template_name, {'form': form,
                                                    'userProfile': userProfile})

    def post(self, request, *args, **kwargs):
        userProfile = get_object_or_404(Profile, user=request.user)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            userProfile.city = form.cleaned_data['city']
            userProfile.phone = form.cleaned_data['phone']
            userProfile.profile_picture = form.cleaned_data['profile_picture']
            userProfile.save()
            return redirect('/user/' + str(request.user.id))
        return render(request, self.template_name, {'form': form,
                                                    'userProfile': userProfile})


@login_required(login_url='/login/')
def messagesView(request):
    friends = Friendship.get_friends(user=request.user)
    friend_users = []
    for friend in friends:
        if friend.user1.id == request.user.id:
            friend_users.append(get_object_or_404(User, id=friend.user2.id))
        else:
            friend_users.append(get_object_or_404(User, id=friend.user1.id))
    return render(request, 'userprofile/messages.html', {'friends': friend_users})


@login_required(login_url='/login/')
def dialogView(request, friend_id):
    form = MessageCreationForm(request.POST)
    return render(request, 'userprofile/dialog.html',
                  {'friend': Profile.objects.get(id=friend_id),
                   'userProfile': Profile.objects.get(id=request.user.id),
                   'form': form})
