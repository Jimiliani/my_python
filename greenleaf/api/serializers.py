from django.contrib.auth.models import User
from rest_framework import serializers
from userprofile.models import PostProfile, PostLike, PostComment, Friendship, GreenLeafUserProfile, Message, \
    FriendshipRequest


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


class FriendshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = '__all__'


class GreenLeafUserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.user.get_full_name()

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
