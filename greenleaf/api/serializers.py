from django.contrib.auth.models import User
from rest_framework import serializers
from userprofile.models import PostProfile, PostLike, PostComment, Friendship, GreenLeafUserProfile, Message


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostProfile
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = '__all__'


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = '__all__'


class GreenLeafUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GreenLeafUserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
