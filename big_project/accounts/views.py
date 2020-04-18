from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.views import generic


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Error: username already created")
                return redirect('/register/')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Error: email already exists")
                return redirect('/register/')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password1)
                user.save()
                messages.info(request, 'User created')
                return redirect('/login/')
        else:
            messages.info(request, "Error: Password doesn't matching")
        return redirect('/register/')
    else:
        return render(request, 'signup/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('http://127.0.0.1:8000/' + str(user.id))
        else:
            messages.info(request, "Error: wrong login or password")
            return redirect('/login/')
    else:
        return render(request, 'signup/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/login/')


class MainpageView(generic.DetailView):
    model = User
    template_name = 'pages/mainpage.html'


class FriendsView(generic.DetailView):
    model = User
    template_name = 'pages/friends.html'
