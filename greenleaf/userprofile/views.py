import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.postgres.aggregates import BoolOr
from django.db.models import Q, F, Count, BooleanField, Value, Case, When
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import logout, login, authenticate

from .models import Profile, ProfilePost, Friendship, Message, PostComment

from .forms import GreenLeafUserCreationForm, GreenLeafUserProfileChangeForm, PostCreationForm


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('/login')


def login_view(request):
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

    def get(self, request, user_id, *args, **kwargs):
        user = User.objects.filter(id=user_id).select_related('profile')[0]
        request_user = User.objects.filter(id=request.user.id).select_related('profile')[0]
        if request.GET and request.GET['request_type'] == 'get_extra_posts':
            posts = ProfilePost.objects.filter(author=user.profile).annotate(
                like_count=Count('like', distinct=True),
                comment_count=Count('comments', distinct=True),
                is_liked_by_user=BoolOr(Case(
                    When(Q(like__user_id=request_user.id), then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )),
            ).values(
                'id',
                'post_text',
                'publication_date',
                'is_liked_by_user',
                'like_count',
                'comment_count',
            ).order_by('-publication_date')[int(request.GET['posts_from']): int(request.GET['posts_to'])]
            return JsonResponse(data={'posts': list(posts)}, status=200)
        if request.GET and request.GET['request_type'] == 'get_comments':
            comments = PostComment.objects.filter(post_id=request.GET['post_id']). \
                values('owner_id', 'text', owner_first_name=F('owner__user__first_name'),
                       owner_last_name=F('owner__user__last_name')).order_by('publication_date')
            return JsonResponse(data={'comments': list(comments)}, status=200)
        is_my_friend = Friendship.are_friends(user=request_user.id, friend=user.id)
        if request.GET and request.GET['request_type'] == 'are_friends':
            return JsonResponse(data={'are_friends': is_my_friend}, status=200)
        posts = ProfilePost.objects.filter(author=user.profile).prefetch_related('like').annotate(
            like_count=Count('like', distinct=True),
            comment_count=Count('comments', distinct=True)
        ).order_by('-publication_date')
        too_many_posts = False
        if posts.count() > 10:
            too_many_posts = True
        posts = posts[:10]
        list(posts)
        form = self.form_class(request.POST)

        args = {'greenLeafUser': user,
                'userProfile': user.profile,
                'posts': posts,
                'form': form,
                'are_friends': is_my_friend,
                'too_many_posts': too_many_posts}
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        if request.POST['request_type'] == 'add_friend':
            Friendship.make_friends(who_adds=int(request.user.id), whom_is_added=int(request.POST['user']))
            return HttpResponse('success')
        elif request.POST['request_type'] == 'delete_friend':
            Friendship.delete_friends(who_delete=int(request.user.id), whom_is_deleted=int(request.POST['user']))
            return HttpResponse('success')
        elif request.POST['request_type'] == 'add_comment':
            PostComment.objects.create(owner_id=request.user.id,
                                       text=request.POST['comment_text'],
                                       post_id=request.POST['post_id'])
            return HttpResponse('success', status=201)
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
        post = get_object_or_404(ProfilePost, id=body.get('post_id'))
        if body['request_type'] == 'add_like':
            post.like.add(request.user.profile)
        elif body['request_type'] == 'remove_like':
            post.like.remove(request.user.profile)
        return JsonResponse(data={'is_liked': request.user.profile in post.like.all(),
                                  'count_of_likes': post.like.count()}, status=201)


class FriendsView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'userprofile/friends.html'

    def get(self, request, *args, **kwargs):
        if 'request_type' not in request.GET:
            return render(request, self.template_name)
        friendships = ''
        if request.GET['request_type'] == 'myFriends':
            friendships = Friendship.objects.select_related('friend1', 'friend2').filter(
                Q(friend1=request.user.profile) | Q(friend2=request.user.profile),
                friend1_agree=True, friend2_agree=True).only('friend1__user_id', 'friend2__user_id',
                                                             'friend1__profile_picture', 'friend2__profile_picture',
                                                             'friend1__user__first_name', 'friend1__user__last_name',
                                                             'friend2__user__first_name', 'friend2__user__last_name')
        elif request.GET['request_type'] == 'incomingRequests':
            friendships = Friendship.objects.select_related('friend1', 'friend2').filter(
                (Q(friend1=request.user.profile) & Q(friend1_agree=False) & Q(friend2_agree=True)) | (
                        Q(friend2=request.user.profile) & Q(friend1_agree=True) & Q(friend2_agree=False))).only(
                'friend1__user_id', 'friend2__user_id',
                'friend1__profile_picture', 'friend2__profile_picture',
                'friend1__user__first_name', 'friend1__user__last_name',
                'friend2__user__first_name', 'friend2__user__last_name')
        elif request.GET['request_type'] == 'outgoingRequests':
            friendships = Friendship.objects.select_related('friend1', 'friend2').filter(
                (Q(friend1=request.user.profile) & Q(friend1_agree=True) & Q(friend2_agree=False)) | (
                        Q(friend2=request.user.profile) & Q(friend1_agree=False) & Q(friend2_agree=True))).only(
                'friend1__user_id', 'friend2__user_id',
                'friend1__profile_picture', 'friend2__profile_picture',
                'friend1__user__first_name', 'friend1__user__last_name',
                'friend2__user__first_name', 'friend2__user__last_name')
        list(friendships)
        if request.GET['request_type'] == 'allUsers':
            profiles = Profile.objects.exclude(user=request.user).select_related('user'). \
                only('user__last_name', 'user__first_name', 'profile_picture', 'user_id')
        else:
            profiles = []
            for friendship in friendships:
                if friendship.friend1_id == request.user.id:
                    profiles.append(friendship.friend2_id)
                else:
                    profiles.append(friendship.friend1_id)
            profiles = Profile.objects.filter(user_id__in=profiles).select_related('user'). \
                only('user__last_name', 'user__first_name', 'profile_picture', 'user_id')
        list(profiles)
        friends = []
        for profile in profiles:
            friends.append({'id': profile.user.id,
                            'full_name': profile.user.first_name + ' ' + profile.user.last_name,
                            'profile_picture': profile.profile_picture.url,
                            'in_friends': Friendship.are_friends(request.user.id, profile.user.id)})
        return JsonResponse(data={'friends': friends}, safe=False, status=200)

    def post(self, request, *args, **kwargs):
        Friendship.make_friends(int(request.user.id), int(request.POST['friend_id']))
        return HttpResponse('success', status=201)

    def delete(self, request, *args, **kwargs):
        body = QueryDict(request.body)
        Friendship.delete_friends(int(request.user.id), int(body.get('friend_id')))
        return HttpResponse('success', status=204)


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
        user_profile = request.user.profile
        form = self.form_class(request.POST, instance=user_profile, initial={'city': user_profile.city,
                                                                             'phone': user_profile.phone})
        return render(request, self.template_name, {'form': form,
                                                    'userProfile': user_profile})

    def post(self, request, *args, **kwargs):
        user_profile = get_object_or_404(Profile, user=request.user)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['city']:
                user_profile.city = form.cleaned_data['city']
            if form.cleaned_data['phone']:
                user_profile.phone = form.cleaned_data['phone']
            if form.cleaned_data['profile_picture']:
                if request.FILES:
                    user_profile.profile_picture = request.FILES['profile_picture']
            user_profile.save()
            return redirect('/user/' + str(request.user.id))
        return render(request, self.template_name, {'form': form,
                                                    'userProfile': user_profile})


class MessagesView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'userprofile/messages.html'

    def get(self, request):
        friendships = Friendship.objects.filter(Q(friend1=request.user.id) | Q(friend2=request.user.id),
                                                friend1_agree=True, friend2_agree=True)
        if request.GET and request.GET['request_type'] == 'has_new_messages':
            if Message.objects.filter(dialog__in=friendships.values_list('id', flat=True), viewed=False).exclude(
                    owner_id=request.user.id).exists():
                return HttpResponse(True)
            else:
                return HttpResponse(False)
        user_profile = request.user.profile
        friendships_where_user_is_friend1 = friendships.filter(friend1=user_profile).select_related('friend2__user'). \
            prefetch_related('messages').annotate(
            friend_id=F('friend2_id'),
            first_name=F('friend2__user__first_name'),
            last_name=F('friend2__user__last_name'),
            new_messages=Case(
                When(Q(messages__viewed=False) & Q(messages__owner_id=F('friend2_id')), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
        ).values('friend_id', 'first_name', 'last_name', 'new_messages').distinct()
        friendships_where_user_is_friend2 = friendships.filter(friend2=user_profile).select_related('friend1__user'). \
            prefetch_related('messages').annotate(
            friend_id=F('friend1_id'),
            first_name=F('friend1__user__first_name'),
            last_name=F('friend1__user__last_name'),
            new_messages=Case(
                When(Q(messages__viewed=False) & Q(messages__owner_id=F('friend1_id')), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
        ).values('friend_id', 'first_name', 'last_name', 'new_messages').distinct()
        profiles = (friendships_where_user_is_friend1 | friendships_where_user_is_friend2)
        args = {'profiles': profiles}
        return render(request, self.template_name, args)


class DialogView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'userprofile/dialog.html'

    def get(self, request, friend_id):
        if 'request_type' not in request.GET:
            user = User.objects.select_related('profile').get(id=friend_id)
            args = {'friend_profile_picture_url': user.profile.profile_picture.url,
                    'friend_full_name': user.get_full_name(),
                    'friend_id': friend_id}
            return render(request, self.template_name, args)
        elif request.GET['request_type'] == 'get_messages':
            friendship = Friendship.objects.get(friend1=min(int(request.user.id), int(friend_id)),
                                                friend2=max(int(request.user.id), int(friend_id)))
            friendship.messages.filter(owner_id=friend_id).update(viewed=True)
            messages = friendship.messages.order_by('publication_date').values(
                'owner_id', 'text', 'publication_date')
            print(messages)
            return JsonResponse(data={'messages': list(messages)})

    def post(self, request, friend_id):
        friendship = Friendship.objects.get(friend1=min(int(request.user.id), int(friend_id)),
                                            friend2=max(int(request.user.id), int(friend_id)))
        Message.objects.create(dialog=friendship, owner_id=request.user.id, text=request.POST['text'])
        return HttpResponse('success')
