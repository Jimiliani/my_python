import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import logout, login, authenticate

from .models import Profile, ProfilePost, Friendship, Message, PostComment

from .forms import GreenLeafUserCreationForm, GreenLeafUserProfileChangeForm, PostCreationForm


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
        if request.GET and request.GET['request_type'] == 'get_extra_posts':
            print('extra_posts')
            posts = ProfilePost.objects.filter(author=user.profile)[
                    int(request.GET['posts_from']):int(request.GET['posts_to'])]
            posts = [post.serialize_extra_posts(request.user.profile) for post in posts.all()]
            return JsonResponse(data={'posts': posts})
        if request.GET and request.GET['request_type'] == 'get_comments':
            comments = []
            for comment in PostComment.objects.filter(post=request.GET['post_id']).order_by('publication_date'):
                comments.append({'owner_id': comment.owner.user.id,
                                 'owner_full_name': comment.owner.user.get_full_name(),
                                 'text': comment.text})
            return JsonResponse(data={'comments': comments}, safe=False)
        are_friends = 'None'
        if user != request.user:
            try:
                Friendship.objects.get(friend1__user_id=min(int(user.id), int(request.user.id)),
                                       friend2__user_id=max(int(user.id), int(request.user.id)))
                are_friends = 'True'
            except Friendship.DoesNotExist:
                are_friends = 'False'
        if request.GET and request.GET['request_type'] == 'are_friends':
            return JsonResponse(data={'are_friends': are_friends})
        user_profile = user.profile
        posts = ProfilePost.objects.filter(author=user_profile)
        too_many_posts = False
        if posts.count() > 10:
            too_many_posts = True
        posts = posts[:10]

        form = self.form_class(request.POST)

        args = {'greenLeafUser': user,
                'userProfile': user_profile,
                'posts': posts,
                'form': form,
                'are_friends': are_friends,
                'too_many_posts': too_many_posts}
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        if request.POST['request_type'] == 'add_friend':
            make_friends(who_adds=int(request.user.id), whom_is_added=int(request.POST['user']))
            return HttpResponse('success')
        elif request.POST['request_type'] == 'delete_friend':
            delete_friends(who_delete=int(request.user.id), whom_is_deleted=int(request.POST['user']))
            return HttpResponse('success')
        elif request.POST['request_type'] == 'add_comment':
            PostComment.objects.create(owner_id=request.user.id,
                                       text=request.POST['comment_text'],
                                       post_id=request.POST['post_id'])
            print(request.POST['comment_text'], request.POST['post_id'])
            print(request.POST['comment_text'], request.POST['post_id'])
            print(request.POST['comment_text'], request.POST['post_id'])
            return HttpResponse('success')
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                post = ProfilePost.objects.create(author=request.user.profile,
                                                  post_text=form.cleaned_data['post_text'])
                return JsonResponse(data={'text': form.cleaned_data['post_text'],
                                          'id': post.id}, status=201)
            return HttpResponse(form=form, status=400)

    def patch(self, request, *args, **kwargs):
        body = json.loads(request.body.decode('utf-8'))
        post = get_object_or_404(ProfilePost, id=body['post_id'])
        if body['request_type'] == 'add_like':
            post.like.add(request.user.profile)
        elif body['request_type'] == 'remove_like':
            post.like.remove(request.user.profile)
        return JsonResponse(data={'is_liked': request.user.profile in post.like.all(),
                                  'count_of_likes': post.like.count()})


class FriendsView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'userprofile/friends.html'

    def get(self, request, *args, **kwargs):
        if 'request_type' not in request.GET:
            return render(request, self.template_name)
        friendships = ''
        if request.GET['request_type'] == 'myFriends':
            friendships = Friendship.objects.filter(Q(friend1=request.user.profile) | Q(friend2=request.user.profile),
                                                    friend1_agree=True, friend2_agree=True)
        elif request.GET['request_type'] == 'incomingRequests':
            friendships = Friendship.objects.filter(
                (Q(friend1=request.user.profile) & Q(friend1_agree=False) & Q(friend2_agree=True)) | (
                        Q(friend2=request.user.profile) & Q(friend1_agree=True) & Q(friend2_agree=False)))
        elif request.GET['request_type'] == 'outgoingRequests':
            friendships = Friendship.objects.filter(
                (Q(friend1=request.user.profile) & Q(friend1_agree=True) & Q(friend2_agree=False)) | (
                        Q(friend2=request.user.profile) & Q(friend1_agree=False) & Q(friend2_agree=True)))
        profiles = []
        for friendship in friendships:
            if friendship.friend1 == request.user.profile:
                profiles.append(friendship.friend2)
            else:
                profiles.append(friendship.friend1)
        if request.GET['request_type'] == 'allUsers':
            profiles = Profile.objects.exclude(user=request.user)
        friends = []
        for profile in profiles:
            print(request.user.profile.friends.all())
            print(profile.friends.all())
            friends.append({'id': profile.user.id,
                            'full_name': profile.user.get_full_name(),
                            'profile_picture': profile.profile_picture.url,
                            'in_friends': are_friends(request.user.id, profile.user.id)})
        return JsonResponse(json.dumps(friends), safe=False)

    def post(self, request, *args, **kwargs):
        make_friends(int(request.user.id), int(request.POST['friend_id']))
        return HttpResponse('success')

    def delete(self, request, *args, **kwargs):
        body = QueryDict(request.body)
        delete_friends(int(request.user.id), int(body.get('friend_id')))
        return HttpResponse('success')


def make_friends(who_adds, whom_is_added):
    try:
        friendship = Friendship.objects.get(
            friend1__user_id=min(who_adds, whom_is_added),
            friend2__user_id=max(who_adds, whom_is_added))
        friendship.friend1_agree = True
        friendship.friend2_agree = True
        friendship.save()
    except Friendship.DoesNotExist:
        friend1 = User.objects.get(id=who_adds).profile
        friend2 = User.objects.get(id=whom_is_added).profile
        if who_adds < whom_is_added:
            Friendship.objects.create(friend1=friend1, friend2=friend2, friend1_agree=True)
        else:
            Friendship.objects.create(friend1=friend2, friend2=friend1, friend2_agree=True)


def delete_friends(who_delete, whom_is_deleted):
    friendship = Friendship.objects.get(
        friend1__user_id=min(who_delete, whom_is_deleted),
        friend2__user_id=max(who_delete, whom_is_deleted))
    if who_delete < whom_is_deleted:
        friendship.friend1_agree = False
    else:
        friendship.friend2_agree = False
    friendship.save()


def are_friends(user, friend):
    try:
        friendship = Friendship.objects.get(friend1__user_id=min(user, friend), friend2__user_id=max(user, friend))
        print('friendship found')
        if friendship.friend1.user.id == user and friendship.friend1_agree or \
                friendship.friend2.user.id == user and friendship.friend2_agree:
            print('true')
            return True
        print('try false')
        return False
    except Friendship.DoesNotExist:
        print('except false')
        return False


# заменить на эту функцию post методы в FriendsView и ProfileWithPkView


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


class MessagesView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'userprofile/messages.html'

    def get(self, request):
        friendships = Friendship.objects.filter(Q(friend1=request.user.profile) | Q(friend2=request.user.profile),
                                                friend1_agree=True, friend2_agree=True)
        profiles = []
        for friendship in friendships:
            profile = ''
            if friendship.friend1 == request.user.profile:
                profile = friendship.friend2
            else:
                profile = friendship.friend1
            profiles.append({'full_name': profile.user.get_full_name(),
                             'id': profile.user.id})
        args = {'profiles': profiles}
        return render(request, self.template_name, args)


class DialogView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'userprofile/dialog.html'

    def get(self, request, friend_id):
        if 'request_type' not in request.GET:
            user = User.objects.get(id=friend_id)
            args = {'friend_profile_picture_url': user.profile.profile_picture.url,
                    'friend_full_name': user.get_full_name(),
                    'friend_id': friend_id}
            return render(request, self.template_name, args)
        elif request.GET['request_type'] == 'get_messages':
            friendship = Friendship.objects.get(friend1=min(int(request.user.id), int(friend_id)),
                                                friend2=max(int(request.user.id), int(friend_id)))
            messages = Message.objects.filter(dialog=friendship)
            serialized_messages = []
            for message in messages:
                serialized_messages.append({'id': message.owner_id,
                                            'text': message.text,
                                            'pub_date': message.publication_date})
            return JsonResponse(data={'messages': serialized_messages})

    def post(self, request, friend_id):
        friendship = Friendship.objects.get(friend1=min(int(request.user.id), int(friend_id)),
                                            friend2=max(int(request.user.id), int(friend_id)))
        Message.objects.create(dialog=friendship, owner_id=request.user.id, text=request.POST['text'])
        return HttpResponse('success')
