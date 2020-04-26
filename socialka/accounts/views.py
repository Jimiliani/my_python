from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.datetime_safe import date

from .forms import UserProfileForm, LoginForm
from .models import Friend, Dialog, SocialPost


@login_required
def home(request):
    posts = SocialPost.objects.filter(sending_time__lte=timezone.now()).order_by('-sending_time')[:10]
    args = {'posts': posts}
    return render(request, 'accounts/home.html', args)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('/accounts')
        else:
            args = {'form': form}
            return render(request, 'accounts/login.html', args)
    else:
        form = LoginForm()
        args = {'form': form}
        return render(request, 'accounts/login.html', args)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/accounts/login')


def register(request):
    stop = False
    if request.method == 'POST':
        if not request.POST['username'] or not request.POST['email'] or not request.POST['password1']:
            messages.info(request, 'Все поля должны быть заполнены!')
            stop = True
        if User.objects.filter(username=request.POST['username']):
            messages.info(request, 'Этот логин уже используется!')
            stop = True
        if User.objects.filter(email=request.POST['email']):
            messages.info(request, 'Этот почтовый адрес уже используется!')
            stop = True
        if request.POST['password1'] != request.POST['password2']:
            messages.info(request, 'Пароли не совпадают!')
            stop = True
        if len(request.POST['password1']) < 8:
            messages.info(request, 'В пароле должно быть не менее 8 символов!')
            stop = True
        if stop:
            return render(request, 'accounts/reg_form.html')
        user = User.objects.create_user(username=request.POST['username'],
                                        first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'],
                                        password=request.POST['password1'])
        user.save()
        return redirect('/accounts/profile')
    else:
        return render(request, 'accounts/reg_form.html')


@login_required
def view_profile(request, pk=None):
    if not User.objects.filter(pk=pk) and pk is not None:
        return redirect('/accounts/profile')
    if pk and User.objects.get(pk=pk) != request.user:
        can_post = False
    else:
        can_post = True
    if request.method == 'POST':
        if request.POST['post_text']:
            SocialPost.objects.create(user_id=request.user.id,
                                      post_text=request.POST['post_text'])
    friend_button = ''
    if pk is not None:
        user = User.objects.get(pk=pk)
        if request.user != user:
            try:
                friends = Friend.objects.get(current_user=request.user.id).users.all()
            except Exception:
                friends = []
            if user not in friends:
                friend_button = 'add'
            else:
                friend_button = 'del'
    else:
        user = request.user
    posts = reversed(SocialPost.objects.filter(user_id=user.id))
    args = {'user': user, 'friend_button': friend_button, 'posts': posts, 'can_post': can_post}
    return render(request, 'accounts/profile.html', args)


@login_required
def view_friends(request):
    try:
        friends = Friend.objects.get(current_user=request.user.id).users.all()
    except Exception:
        friends = []
    users = User.objects.all().exclude(id=request.user.id).order_by('last_name')
    args = {'users': users,
            'friends': friends}
    return render(request, 'accounts/friends.html', args)


@login_required
def change_friends(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if request.user != new_friend:
        if operation == 'add':
            Friend.make_friend(request.user, new_friend)
        elif operation == 'lose':
            Friend.lose_friend(request.user, new_friend)
    return redirect('/accounts/friends')


@login_required
def view_messages(request):
    try:
        friends = Friend.objects.get(current_user=request.user.id).users.all()
    except Exception:
        friends = []
    args = {'friends': friends}
    return render(request, 'accounts/messages.html', args)


@login_required
def view_dialog(request, pk):
    user_to = User.objects.get(pk=pk)
    try:
        friends = Friend.objects.get(current_user=request.user.id).users.all()
    except Exception:
        friends = []

    if user_to not in friends:
        return redirect('/accounts/messages')

    if request.method == 'POST' and request.POST['message_text']:
        Dialog.objects.create(message_from_id=request.user.id,
                              message_to_id=user_to.id,
                              message_text=request.POST['message_text'],
                              sending_time=date.today())

    messages = reversed(Dialog.objects.filter(message_to_id__in=[request.user.id, user_to.id],
                                              message_from_id__in=[request.user.id, user_to.id]))
    args = {'user_to': user_to,
            'user_from': request.user,
            'friends': friends,
            'messages': messages}
    return render(request, 'accounts/dialog.html', args)


@login_required
def edit_profile(request):
    form = UserProfileForm(instance=request.user.userprofile)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
    args = {'form': form}
    return render(request, 'accounts/edit_profile.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile')
        else:
            args = {'form': form}
            return render(request, 'accounts/change_password.html', args)
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)
