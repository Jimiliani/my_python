from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from userprofile.forms import MessageCreationForm
from userprofile.models import GreenLeafUserProfile, Message, FriendshipRequest
from .serializers import *


class PostList(LoginRequiredMixin, APIView):
    login_url = '/login/'

    def get(self, request):
        posts = PostProfile.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListWithUserId(LoginRequiredMixin, APIView):
    def get(self, request, user_id):
        try:
            posts = PostProfile.objects.get(author__id=int(user_id))
            serializer = PostSerializer(posts, many=False)
        except PostProfile.DoesNotExist:
            return Response()
        return Response(serializer.data)


class FriendshipListWithFriendId(LoginRequiredMixin, APIView):
    login_url = '/login/'

    def get(self, request, friend_id):
        friend = User.objects.get(id=friend_id)
        if Friendship.are_friends(request.user, friend) or FriendshipRequest.has_friend_request(user_from=request.user,
                                                                                                user_to=friend):
            return Response(True)
        return Response(False)

    def post(self, request, friend_id):
        friend = User.objects.get(id=friend_id)
        if FriendshipRequest.has_friend_request(user_from=friend, user_to=request.user):
            friendship_request = FriendshipRequest.objects.get(user_from=friend, user_to=request.user)
            friendship_request.delete()
            serializer = FriendshipSerializer(data=request.data)
        else:
            _mutable = request.data._mutable
            request.data._mutable = True
            request.data['user_from'] = request.user.id
            request.data['user_to'] = friend_id
            request.data._mutable = _mutable
            serializer = FriendshipRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, friend_id):
        friend = User.objects.get(id=friend_id)
        if Friendship.are_friends(request.user, friend):
            friendship = Friendship.get_friendship(user1=request.user, user2=friend)
            friendship.delete()
            _mutable = request.data._mutable
            request.data._mutable = True
            request.data['user_from'] = friend_id
            request.data['user_to'] = request.user.id
            request.data._mutable = _mutable
            serializer = FriendshipRequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
        else:
            friendship_request = FriendshipRequest.objects.get(user_from=request.user, user_to=friend)
            friendship_request.delete()
        return Response(True)


class FriendshipList(LoginRequiredMixin, APIView):
    login_url = '/login/'

    def get(self, request):
        confirmed_friends = Friendship.get_friends(request.user)
        user_items = []
        if request.GET['requestType'] == 'myFriends':
            for friend in confirmed_friends:
                if friend.user1 == request.user:
                    user_items.append(get_object_or_404(GreenLeafUserProfile, user=friend.user2))
                else:
                    user_items.append(get_object_or_404(GreenLeafUserProfile, user=friend.user1))
        elif request.GET['requestType'] == 'allUsers':
            user_items = GreenLeafUserProfile.objects.exclude(id=request.user.id)
        elif request.GET['requestType'] == 'outgoingRequests':
            outgoing_requests = FriendshipRequest.objects.filter(user_from=request.user)
            for friend in outgoing_requests:
                user_items.append(get_object_or_404(GreenLeafUserProfile, user=friend.user_to))
        elif request.GET['requestType'] == 'incomingRequests':
            incoming_requests = FriendshipRequest.objects.filter(user_to=request.user)
            for friend in incoming_requests:
                user_items.append(get_object_or_404(GreenLeafUserProfile, user=friend.user_from))
        else:
            return Response()
        serializer = GreenLeafUserProfileSerializer(user_items, many=True)
        return Response(serializer.data)


class LikeList(LoginRequiredMixin, APIView):
    login_url = '/login/'

    def get(self, request, post_id):
        try:
            likes = PostLike.objects.filter(post_id=post_id)
        except PostProfile.DoesNotExist:
            likes = []
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data['owner'] = request.user.id
        request.data['post'] = post_id
        request.data._mutable = _mutable
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        try:
            like = PostLike.objects.get(post_id=post_id, owner_id=request.user.id)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Friendship.DoesNotExist:
            return Response()


class DialogView(LoginRequiredMixin, APIView):
    login_url = '/login/'
    form_class = MessageCreationForm
    template_name = 'userprofile/dialog.html'

    def get(self, request, friend_id, *args, **kwargs):
        user_profile = GreenLeafUserProfile.objects.get(user=request.user)
        friend_profile = GreenLeafUserProfile.objects.get(id=friend_id)
        messages = Message.objects.none()
        messages = reversed(messages.union(
            Message.objects.filter(message_from=user_profile, message_to=friend_profile),
            Message.objects.filter(message_from=friend_profile, message_to=user_profile)).order_by('-time')[:20])
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
