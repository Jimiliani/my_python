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
                messages.info(request, "Этот логин уже используется, введите другой")
                return redirect('/register/')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Эта почта уже используется, введите другую")
                return redirect('/register/')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password1)
                user.save()
                messages.info(request, 'User created')
                return redirect('/login/')
        else:
            messages.info(request, "Пароли не совпадают")
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

    def post(self, request, pk):
        if request.POST['friend_id'] == '':
            messages.info(request, "Вы не ввели id")
        elif int(request.user.id) == int(request.POST['friend_id']):
            messages.info(request, "Вы не можете стать другом самому себе")
        elif User.objects.filter(id=request.POST['friend_id']):
            # print(User.objects.filter(id=request.POST['friend_id']))
            # print(User.objects.filter(id=request.POST['friend_id'])[0])
            # request.user.friends_set.add(User.objects.filter(id=request.POST['friend_id'])[0])
            messages.info(request,
                          "Вы отправили(нет) заявку пользователю " +
                          User.objects.filter(id=request.POST['friend_id'])[0].get_full_name())
        else:
            messages.info(request, "Нет человека с таким id!")
        return render(request, self.template_name)
