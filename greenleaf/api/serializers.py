from rest_framework import serializers
from userprofile.models import PostProfile, PostLike, PostComment


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
