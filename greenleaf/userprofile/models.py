from django.contrib.auth.models import User
from django.db import models


class GreenLeafUserProfile(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    profile_picture = models.ImageField(default='/pictures/default.png', upload_to='pictures')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=63, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return str(self.user)


class ProfilePost(models.Model):
    post_text = models.TextField(max_length=5000)
    author = models.ForeignKey(GreenLeafUserProfile, on_delete=models.CASCADE)
