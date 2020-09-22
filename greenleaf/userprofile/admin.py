from django.contrib import admin
from .models import Profile, ProfilePost, Friendship, Message

admin.site.register(Profile)
admin.site.register(ProfilePost)
admin.site.register(Friendship)
admin.site.register(Message)
