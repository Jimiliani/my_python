from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth


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
                return redirect('/register/')
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
            return redirect('/me/')
        else:
            messages.info(request, "Error: wrong login or password")
            return redirect('/login/')
    else:
        return render(request, 'signup/login.html')


def mainpage(request):
    if request.user.is_authenticated:
        messages.info(request, str(request.user))
        if request.method == 'Post':
            print(request.user)
            messages.info(request, str(request.user))
        else:
            return render(request, 'pages/mainpage.html')
    else:
        return redirect('/login/')


def logout(request):
    auth.logout(request)
    return redirect('/login/')


def friends(request):
