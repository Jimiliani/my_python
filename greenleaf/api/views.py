from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from userprofile.forms import MessageCreationForm
from userprofile.models import GreenLeafUserProfile, Message
from .serializers import *


class PostList(APIView):
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


class PostListWithUserId(APIView):
    def get(self, request, user_id):
        try:
            posts = PostProfile.objects.get(author__id=int(user_id))
            serializer = PostSerializer(posts, many=False)
        except PostProfile.DoesNotExist:
            return Response()
        return Response(serializer.data)


class FriendshipListWithFriendId(APIView):
    def get(self, request, friend_id):
        try:
            friends = Friendship.objects.get(owner_id=request.user.id, friend_id=friend_id)
        except Friendship.DoesNotExist:
            friends = []
        serializer = FriendshipSerializer(friends, many=False)
        return Response(serializer.data)

    def post(self, request, friend_id):
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data['owner'] = request.user.id
        request.data['friend'] = friend_id
        request.data._mutable = _mutable
        serializer = FriendshipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, friend_id):
        try:
            friendship = Friendship.objects.get(owner_id=request.user.id, friend_id=friend_id)
            friendship.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Friendship.DoesNotExist:
            return Response()


class FriendshipList(APIView):
    def get(self, request):
        all_friendships = Friendship.objects.filter(owner=request.user)
        confirmed_friends = Friendship.objects.none()
        user_items = []
        for friend in all_friendships:
            confirmed_friends = confirmed_friends.union(
                Friendship.objects.filter(owner=friend.friend, friend=friend.owner))
        if request.GET['requestType'] == 'myFriends':
            for friend in confirmed_friends:
                if friend.owner.id != request.user.id:
                    if request.GET['contentType'] == 'users':
                        user_items.append(get_object_or_404(User, id=friend.owner.id))
                    elif request.GET['contentType'] == 'userprofiles':
                        user_items.append(get_object_or_404(GreenLeafUserProfile, user=friend.owner))
        elif request.GET['requestType'] == 'allUsers':
            if request.GET['contentType'] == 'users':
                user_items = User.objects.exclude(id=request.user.id)
            elif request.GET['contentType'] == 'userprofiles':
                user_items = GreenLeafUserProfile.objects.exclude(id=request.user.id)
        elif request.GET['requestType'] == 'outgoingRequests':
            partly_friends = Friendship.objects.filter(owner=request.user).difference(confirmed_friends)
            # partly_friends = all_friendships
            # partly_friends = confirmed_friends
            for friend in partly_friends:
                if request.GET['contentType'] == 'users':
                    user_items.append(get_object_or_404(User, id=friend.friend.id))
                elif request.GET['contentType'] == 'userprofiles':
                    user_items.append(get_object_or_404(GreenLeafUserProfile, user=friend.friend))
        elif request.GET['requestType'] == 'incomingRequests':
            partly_friends = Friendship.objects.filter(friend=request.user).difference(confirmed_friends)
            for friend in partly_friends:
                if request.GET['contentType'] == 'users':
                    user_items.append(get_object_or_404(User, id=friend.owner.id))
                elif request.GET['contentType'] == 'userprofiles':
                    user_items.append(get_object_or_404(GreenLeafUserProfile, user=friend.owner))
        else:
            return Response()
        if request.GET['contentType'] == 'users':
            serializer = UserSerializer(user_items, many=True)
        else:
            serializer = GreenLeafUserProfileSerializer(user_items, many=True)
        return Response(serializer.data)


class LikeList(APIView):
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


class DialogView(APIView):
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
