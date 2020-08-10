from django.contrib import admin
from .models import GreenLeafUserProfile, PostProfile, Friendship, PostLike

admin.site.register(GreenLeafUserProfile)
admin.site.register(PostProfile)
admin.site.register(Friendship)
admin.site.register(PostLike)
