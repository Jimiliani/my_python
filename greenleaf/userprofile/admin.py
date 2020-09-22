from django.contrib import admin
from .models import Profile, ProfilePost, Friendship, PostLike, Message

admin.site.register(Profile)
admin.site.register(ProfilePost)
admin.site.register(Friendship)
admin.site.register(PostLike)
admin.site.register(Message)
